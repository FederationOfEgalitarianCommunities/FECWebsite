"""This module contains views to display Documents and their Categories."""
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404

from mezzanine.generic.models import Keyword

from .models import Document, DocumentCategory


class DocumentDetail(DetailView):
    """Shows the details of a publish :class:`~.models.Document`.

    The :class:`~.models.Document` is passed in to the template as the
    ``document`` and ``editable_obj`` context variables.

    The default template is ``documents/document_details.html``

    """
    context_object_name = 'document'
    template_name = 'documents/document_details.html'

    def get_queryset(self):
        """Limit the available Documents to published documents."""
        return Document.objects.published(for_user=self.request.user)

    def get_context_data(self, **kwargs):
        """Add the Document to the context as an ``editable_obj``."""
        context = super(DocumentDetail, self).get_context_data(**kwargs)
        context['editable_obj'] = context['document']
        return context


class DocumentCategoryDetail(DetailView):
    """Shows the details of a :class:`~.models.DocumentCategory`.

    The :class:`~.models.DocumentCategory` is passed in to the template as the
    ``document_category`` context variable. It is also set to the
    ``editable_obj`` variable for the ``editable`` admin link.

    The default template is ``documents/category_details.html``.

    """
    model = DocumentCategory
    context_object_name = 'document_category'
    template_name = 'documents/category_details.html'

    def get_context_data(self, **kwargs):
        """Add the DocumentCategory to the context as an ``editable_obj``."""
        context = super(DocumentCategoryDetail,
                        self).get_context_data(**kwargs)
        context['editable_obj'] = context['document_category']
        return context


class RootDocumentCategoryList(ListView):
    """Shows a listing of all root :class:`~.models.DocumentCategory`.

    They are passed in with the ``root_categories`` context variable.

    The default template is ``documents/root_categories.html``.

    """
    context_object_name = 'root_categories'
    template_name = 'documents/root_categories.html'

    def get_queryset(self):
        """Return only Categories with no parent."""
        return DocumentCategory.objects.filter(parent=None).prefetch_related(
            'children', 'documents', 'children__documents')


class DocumentTagList(ListView):
    """Shows a listing of :class:`.models.Document <Documents>` for a keyword.

    The keyword should be passed in with the ``tag`` kwarg.

    The default template is ``documents/document_tag_list.html``.

    """
    context_object_name = 'documents'
    template_name = 'documents/document_tag_list.html'

    def get_queryset(self):
        """Return only Documents with the specified ``tag``."""
        tag = get_object_or_404(Keyword, slug=self.kwargs['tag'])
        return Document.objects.filter(keywords__keyword=tag)

    def get_context_data(self, **kwargs):
        """Add the tag name to the context."""
        context = super(DocumentTagList, self).get_context_data(**kwargs)
        context['tag'] = get_object_or_404(Keyword, slug=self.kwargs['tag'])
        return context
