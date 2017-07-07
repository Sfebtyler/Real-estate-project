from app.models import Home, ExtraImage, ContactInfo, Favorites
from django.db.models import Q
from django.views import generic as generic_views
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse


class UserLogin(generic_views.ListView):

    def post(self, request, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        next_page = request.POST.get('next')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            return HttpResponseRedirect(next_page or reverse('mainpage'))
        else:
            return 'invalid login'


class UserLogout(generic_views.ListView):

    def post(self, request, **kwargs):
        next_page = request.POST.get('next')
        logout(request)
        return HttpResponseRedirect(next_page or reverse('mainpage'))


class UserCreateTemplateView(generic_views.TemplateView):
    template_name = 'logincreate/create.html'
    context_object_name = 'create'


class PremiumHomeTemplateView(generic_views.ListView):
    template_name = 'main_page/main_page.html'
    context_object_name = 'homes'

    def get_queryset(self):
        qset = Home.objects.filter(published=True)
        qset = qset.filter(is_premium=True)
        return qset


class HomeTemplateView(generic_views.ListView):
    template_name = 'homes_page/homes_page.html'
    context_object_name = 'homes'

    def get_queryset(self):
        qset = Home.objects.all()
        if not self.request.GET.get('q'):
            return Home.objects.filter(published=True)
        else:
            params = self.request.GET['q']
            if params:

                # Poor mans search endpoint
                search_term = params.strip()


                qset = qset.filter(
                    Q(title__icontains=search_term) |
                    Q(city__icontains=search_term) |
                    Q(street__icontains=search_term) |
                    Q(mlsnumber__number__icontains=search_term)
                )
                return qset.distinct()


class HomeDetailsTemplateView(generic_views.ListView):
    template_name = 'details_page/details_page.html'
    context_object_name = 'details'

    def get_queryset(self):
        qset = Home.objects.get(pk=self.kwargs['id'])
        if ExtraImage.objects.filter(home=self.kwargs['id']).exists():
            qset.extrainfo = ExtraImage.objects.get(home=self.kwargs['id'])
        else:
            return qset
        return qset


class FavoritesHomeTemplateView(generic_views.ListView):
    template_name = 'favorites/favorites_page.html'
    context_object_name = 'favorites'

    def post(self, request, **kwargs):
        print(self.request.POST)
        home = self.request.POST.get('homepk')
        next_page = request.POST.get('next')
        if len(self.request.user.favorites.filter(pk=home)) > 0:
            Favorites.objects.get(list=home).delete()
            return HttpResponseRedirect(next_page)
        else:
            newfav = Favorites(user=self.request.user, list=Home.objects.get(pk=home))
            newfav.save()
            return HttpResponseRedirect(next_page)

    def get_queryset(self):
        return self.request.user.favorites.all()


class SearchHomesTemplateView(generic_views.ListView):
    template_name = 'search/search_page.html'
    context_object_name = 'results'

    def get_queryset(self):
        qset = Home.objects.all()
        params = self.request.GET
        if params:

            if params['totalbeds'] and params['totalbeds'] != '':
                qset = qset.filter(
                    Q(numofbeds__icontains=params['totalbeds'])
                )

            if params['totalbaths'] and params['totalbaths'] != '':
                qset = qset.filter(Q(numofbaths__icontains=params['totalbaths'])
                                   )

            if params['pricerangestart'] and params['pricerangestart'] != '':
                qset = qset.filter(Q(price__gte=params['pricerangestart'])
                                   )

            if params['pricerangestop'] and params['pricerangestop'] != '':
                qset = qset.filter(Q(price__lte=params['pricerangestop'])
                                   )

            if params['pricerangestart'] and params['pricerangestop'] and params['pricerangestart'] != '' and \
                            params['pricerangestop'] != '':
                qset = qset.filter(Q(price__range=(params['pricerangestart'], params['pricerangestop'])))

            if params['q']:
                # Poor mans search endpoint
                search_term = params['q'].strip()

                qset = qset.filter(
                    Q(title__icontains=search_term) |
                    Q(city__icontains=search_term) |
                    Q(street__icontains=search_term) |
                    Q(mlsnumber__number__icontains=search_term)
                )
                return qset.distinct()
            return qset


class ContactsTemplateView(generic_views.ListView):
    template_name = 'contacts/contacts_page.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        return ContactInfo.objects.first()
