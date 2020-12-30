from uuid import UUID

from django.db.models import Model, QuerySet
from django.shortcuts import get_object_or_404


def get_all_model_entries(model: Model) -> QuerySet:
    """Return queryset with all model entries"""
    return model.objects.all()


def get_concrete_model_entry_by_pk(model: Model, pk: UUID) -> Model:
    """Return a concrete model entry with pk"""
    return get_object_or_404(model, pk=pk)
