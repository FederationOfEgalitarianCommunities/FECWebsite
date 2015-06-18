"""This module contains views used to display Communities."""
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView

from .models import Community


class PublishedCommunityMixin(object):
    """An abstraction limiting the objects to published communities."""
    def get_queryset(self):
        """Limit the available Communities to published communities."""
        return Community.objects.published(for_user=self.request.user)


class AbstractCommunityDetail(PublishedCommunityMixin, DetailView):
    """An abstraction of the Community and CommunityInDialog DetailViews.

    The :class:`~.models.Community` is passed to the template as the
    ``community`` context variable. It is also set to the ``editable_obj``
    variable so that the
    :func:`mezzanine.core.templatetags.mezzanine_tags.editable_loader`
    templatetag properly sets the ``ADMIN`` link.

    The default template is ``community/details.html``.

    """
    context_object_name = "community"
    template_name = "communities/details.html"

    def get_context_data(self, **kwargs):
        """Add the Community to the context as an ``editable_obj``."""
        context = super(AbstractCommunityDetail,
                        self).get_context_data(**kwargs)
        context['editable_obj'] = context['community']
        return context


class CommunityDetail(AbstractCommunityDetail):
    """Shows the details of a published :class:`~.models.Community`."""
    def get(self, request, slug, *args, **kwargs):
        """Redirect non-Members to the correct detail view.."""
        community = get_object_or_404(Community, slug=slug)
        if community.membership_status != Community.MEMBER:
            return redirect(community.get_absolute_url())
        return super(CommunityDetail, self).get(request, slug, *args, **kwargs)


class CommunityInDialogDetail(AbstractCommunityDetail):
    """Shows the details of a published ``Community in Dialog``.

    This is represented by the :class:`~.models.Community` model's
    :attr:`~.models.Community.membership_status` attribute.

    """
    def get(self, request, slug, *args, **kwargs):
        """Redirect non-Communities-in-Dialog to the correct detail view.."""
        community = get_object_or_404(Community, slug=slug)
        if community.membership_status != Community.COMMUNITY_IN_DIALOG:
            return redirect(community.get_absolute_url())
        return super(CommunityInDialogDetail, self).get(
            request, slug, *args, **kwargs)


class AllyCommunityDetail(AbstractCommunityDetail):
    """Shows the details of a published ``Ally Community``.

    This is represented by the :class:`~.models.Community` model's
    :attr:`~.models.Community.membership_status` attribute.

    """
    def get(self, request, slug, *args, **kwargs):
        """Redirect non-Allies to the correct detail view."""
        community = get_object_or_404(Community, slug=slug)
        if community.membership_status != Community.ALLY:
            return redirect(community.get_absolute_url())
        return super(AllyCommunityDetail, self).get(
            request, slug, *args, **kwargs)


class CommunityList(PublishedCommunityMixin, ListView):
    """Shows a listing of all FEC Communities and Communities in Dialog.

    The following lists of :class:`.models.Community <Communities>` are
    available to the template:

    * ``community_list`` - Member Communities
    * ``in_dialog_list`` - Communities in Dialog

    The default template is ``community/list.html``.

    """
    model = Community
    context_object_name = "community_list"
    template_name = "communities/list.html"

    def get_context_data(self, **kwargs):
        """Modify the context to filter the Community lists."""
        context = super(CommunityList, self).get_context_data(**kwargs)
        context['community_list'] = Community.objects.filter(
            membership_status=Community.MEMBER)
        context['in_dialog_list'] = Community.objects.filter(
            membership_status=Community.COMMUNITY_IN_DIALOG)
        context['ally_list'] = Community.objects.filter(
            membership_status=Community.ALLY)
        return context
