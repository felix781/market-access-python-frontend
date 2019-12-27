from django.urls import reverse

from utils.api_client import MarketAccessAPIClient


class BarrierContextMixin:
    include_interactions = True
    _barrier = None

    @property
    def barrier(self):
        if not self._barrier:
            self._barrier = self.get_barrier()
        return self._barrier

    def get(self, request, *args, **kwargs):
        if self.include_interactions:
            self.interactions = self.get_interactions()
        return super().get(request, *args, **kwargs)

    def get_barrier(self):
        client = MarketAccessAPIClient(self.request.session.get('sso_token'))
        barrier_id = self.kwargs.get('barrier_id')
        return client.barriers.get(id=barrier_id)

    def get_interactions(self):
        client = MarketAccessAPIClient(self.request.session.get('sso_token'))
        barrier_id = self.kwargs.get('barrier_id')
        notes = client.interactions.list(barrier_id=barrier_id)
        history = client.barriers.get_history(barrier_id=barrier_id)
        interactions = notes + history

        if self.barrier.has_assessment:
            interactions += client.barriers.get_assessment_history(
                barrier_id=barrier_id
            )

        interactions.sort(key=lambda object: object.date, reverse=True)

        return interactions

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['barrier'] = self.barrier
        if self.include_interactions:
            context_data['interactions'] = self.interactions
        return context_data


class TeamMembersContextMixin:
    _team_members = None

    def get_team_members(self):
        if self._team_members is None:
            client = MarketAccessAPIClient(
                self.request.session.get('sso_token')
            )
            self._team_members = client.barriers.get_team_members(
                barrier_id=self.kwargs.get('barrier_id')
            ).get('results', [])

        return self._team_members

    def get_team_member(self, team_member_id):
        for member in self.get_team_members():
            if member['id'] == team_member_id:
                return member

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['team_members'] = self.get_team_members()
        return context_data


class APIFormMixin:
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        if hasattr(self, 'object'):
            return self.object.to_dict()
        return {}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(self.kwargs)
        kwargs['token'] = self.request.session.get('sso_token')
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.object:
            context_data['object'] = self.object
        return context_data


class APIBarrierFormMixin(APIFormMixin):
    def get_object(self):
        client = MarketAccessAPIClient(self.request.session.get('sso_token'))
        barrier_id = self.kwargs.get('barrier_id')
        return client.barriers.get(id=barrier_id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['id'] = kwargs.pop('barrier_id')
        return kwargs

    def get_success_url(self):
        return reverse(
            'barriers:barrier_detail',
            kwargs={'barrier_id': self.kwargs.get('barrier_id')}
        )
