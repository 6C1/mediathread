from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden

from django.shortcuts import get_object_or_404


from modelversions import _rebuild_from_version as rebuild
from django.db.models import get_model

from tagging.models import Tag
from tagging.utils import calculate_cloud

from assetmgr.lib import annotated_by


Asset = get_model('assetmgr','asset')
SherdNote = get_model('djangosherd','sherdnote')
Project = get_model('projects','project')
ProjectVersion = get_model('projects','projectversion')
User = get_model('auth','user')
        

from courseaffils.lib import in_course_or_404
from projects.forms import ProjectForm
from djangohelpers.lib import rendered_with
from djangohelpers.lib import allow_http

@rendered_with('projects/project.html')
def project_workspace(request, user, project):
    space_viewer = request.user
    if request.GET.has_key('as') and request.user.is_staff:
        space_viewer = get_object_or_404(User, username=request.GET['as'])

    assets = annotated_by(Asset.objects.filter(course=request.course),
                          space_viewer)

    projectform = ProjectForm(request, instance=project)
    
    return {
        'is_space_owner': project.is_participant(user),
        'space_owner': user,
        'space_viewer': space_viewer,
        'project': project,
        'projectform': projectform,
        'assets': assets,
        'page_in_edit_mode': True,
        }

@rendered_with('projects/published_project.html')
def project_preview(request, user, project):
    return {
        'is_space_owner': project.is_participant(user),
        'project': project,
        'is_preview': True,
        }
        
        

@rendered_with('projects/preview_project.html')
def project_version_preview(request, user_name, project_id, version_id):
    #import pdb
    project = get_object_or_404(Project, pk=project_id, course=request.course)
    space_owner = in_course_or_404(user_name, request.course)
    version = ProjectVersion.objects.get(version_number=version_id)
    rebuild(version, project)
    return {
        'project': project,
        'space_owner': project.author,
        'version_id': int(version_id),
        'all_version_ids':  [p.version_number for p in  project.versions]
        }
        
        

@rendered_with('projects/published_project.html')
@allow_http("GET")
def project_readonly_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id,
                                course=request.collaboration_context.content_object,
                                submitted=True)
    return {
        'is_space_owner': project.is_participant(request),
        'space_owner': project.author,
        'project': project,
        }

@allow_http("GET", "POST", "DELETE")
def view_project(request, user_name, project_id):
    space_owner = in_course_or_404(user_name, request.course)

    project = get_object_or_404(Project, pk=project_id,
                                course=request.course)

    if project not in Project.get_user_projects(space_owner,request.course):
        return HttpResponseForbidden("forbidden")



    if request.method == "DELETE":
        project.delete()
        return HttpResponseRedirect(
            reverse('your-space-projects', args=[user_name]))

    if request.method == "GET":
        if project.is_participant(request.user):
            return project_workspace(request, space_owner, project)
        else:
            return project_readonly_view(request, project.id)

    
    if request.method == "POST":
        projectform = ProjectForm(request, instance=project,data=request.POST)
        redirect_to = '.'
        if projectform.is_valid():
            if "Submit"== request.POST.get('submit',None):
                projectform.instance.submitted = True
                redirect_to = reverse('your-space-projects', args=[user_name])
                redirect_to += "?show=%d" % project.pk
                
            projectform.save()

        if "Preview" == request.POST.get('submit',None):
            return project_preview(request, space_owner, project)

        return HttpResponseRedirect(redirect_to)

@rendered_with('projects/your_projects.html')
@allow_http("GET", "POST")
def your_projects(request, user_name):
    in_course_or_404(user_name, request.course)
    
    user = get_object_or_404(User, username=user_name)

    editable = user==request.user

    if request.method == "GET":
        projects = Project.get_user_projects(user, request.course)
        if not editable:
            projects = projects.filter(submitted=True)
        projects = projects.order_by('modified')

        try:
            initially_expanded_project = int(request.GET['show'])
        except:
            if len(projects):
                initially_expanded_project = projects[0].pk
            else:
                initially_expanded_project = None
        
        return {
            'projects': projects,
            'editable': editable,
            'space_owner': user,
            'initially_expanded_project': initially_expanded_project,
            }

    if request.method == "POST":
        if not editable:
            return HttpResponseForbidden("forbidden")
        
        title = request.POST.get('title', "Add title here" % user)
        project = Project(author=user, course=request.course, title=title)
        project.save()
        return HttpResponseRedirect(project.get_absolute_url())