from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Course, Category, CourseReview
from .forms import CourseForm, CourseReviewForm


def all_courses(request):
    """ A view to show all courses available, including sorting and searching queries """

    courses = Course.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                courses = courses.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            courses = courses.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            courses = courses.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('courses'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            courses = courses.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'courses': courses,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'courses/courses.html', context)

def course_detail(request, course_id):
    """ A view to show individual course details """
    course = get_object_or_404(Course, pk=course_id)
    form = CourseReview

    if request.method == 'POST':
        form = CourseReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.course = course
            form.save()
            messages.success(request, 'Your review has been sent to Admin for approval!')
            context = {
                'course': course,
                'form': form,
            }

            return render(request, 'courses/course_detail.html', context)
        else:
            messages.error(request, 'Failed to add the review. Please, make sure the form is valid!')
    else:
        form = CourseReviewForm()
        context = {
                'course': course,
                'form': form,
            }
    return render(request, 'courses/course_detail.html', context)


@login_required
def add_course(request):
    """
    Add a course to the store
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only Store Management can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            messages.success(request, 'Successfully added course!')
            return redirect(reverse('course_detail', args=[course.id]))
        else:
            messages.error(request, 'Failed to add a new course. Please, make sure the form is valid!')
    else:
        form = CourseForm()

    template = 'courses/add_course.html'
    context = {
        'form': form,
    }
    
    return render(request, template, context)

@login_required
def edit_course(request, course_id):
    """
    Edit a course in the store
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only Store Management can do that.')
        return redirect(reverse('home'))

    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Updated Course!')
            return redirect(reverse('course_detail', args=[course.id]))
        else:
            messages.error(request, 'Failed to update the course. Please, make sure the form is valid!')
    else:
        form = CourseForm(instance=course)
        messages.info(request, f'You are editing {course.name}')

    template = 'courses/edit_course.html'
    context = {
        'form': form,
        'course': course,
    }
    
    return render(request, template, context)

@login_required
def delete_course(request, course_id):
    """
    Delete a course from store
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only Store Management can do that.')
        return redirect(reverse('home'))
        
    course = get_object_or_404(Course, pk=course_id)
    course.delete()
    messages.success(request, 'Course has been deleted!')
    return redirect(reverse('courses'))


@login_required
def delete_review(request, review_id, ):
    """
    Delete the course review
    """
    review = get_object_or_404(CourseReview, id=review_id)

    if request.user == review.user:
        review.delete()
        messages.success(request, 'The review has been deleted!')

        return redirect('course_detail', review.course.id)
    else:
        messages.error(request, 'Failed to delete the review. Please, make sure that you have permission!')

    return redirect('course_detail', review.course.id)


def edit_review(request, review_id):
    """
    Edit a course review
    """
    review = get_object_or_404(CourseReview, id=review_id)
    course = get_object_or_404(Course, pk=review.course.id)
    form = CourseReviewForm(instance=review)

    if request.method == 'POST':
        form = CourseReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review has been successfully edited!')
            context = {
                'course': course,
                'review': review,
                'form': form,
            }
            return redirect('course_detail', review.course.id)
        else:
            messages.error(request, 'Failed to add the review. Please, make sure the form is valid!')
            
            form = CourseReviewForm(instance=review)
            context = {
                'course': course,
                'review': review,
                'form': form,
            }
    else:
        form = CourseReviewForm(instance=review)
        messages.info(request, f'You are editing "{review.title}"')
        context = {
            'course': course,
            'review': review,
            'form': form,
        }
        return render(request, 'courses/course_detail.html', context)

    return render(request, 'courses/course_detail.html', context)