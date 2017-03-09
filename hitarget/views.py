from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
import pprint as pp

from django.urls import reverse

from hitarget.hitarget_faker import fake_lead_add_form_data
from .models import Lead
from .forms import AddLeadForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext as _


# Create your views here.



def blank(request):
    #     only for development! used as a template for bracket
    return render(
        request=request,
        template_name="hitarget/base.html"
    )


def home(request):
    leads = Lead.objects.all()[0:10]
    return render(
        request=request,
        template_name="hitarget/leads/home.html",
        context={"leads": [lead_mini(request, lead=l) for l in leads]}
    )


def lead_mini(request, lead):
    ff = loader.render_to_string(
        request=request,
        template_name="hitarget/components/lead_mini.html",
        context={"lead": lead, "associated_actions": lead.generate_action_buttons_mini(request)}
    )
    return ff


@login_required
def lead_detail(request, slug):
    lead = get_object_or_404(Lead, slug=slug)
    return render(
        request=request,
        template_name="hitarget/leads/detail.html",
        context={
            "lead_html": lead_maxi(request, lead),
            "lead": lead,
        }
    )


@login_required
def lead_maxi(request, lead):
    return loader.render_to_string(
        request=request,
        template_name="hitarget/components/lead_maxi.html",
        context={"lead": lead, "associated_actions": lead.generate_action_buttons_maxi(request)}
    )


@login_required
def lead_detail_full(request, slug):
    print("getting %s", slug)
    lead = get_object_or_404(Lead, slug=slug)
    if lead.author == request.user:
        messages.info(request, _("Seul vous pouvez voir ces infos"))
    else:
        # TODO add check that lead is actually bought
        messages.info(request, _("Félicitations, ce lead est à vous!"))
    return render(
        request=request,
        template_name="hitarget/leads/detail_full.html",
        context={
            "lead_html": lead_full(request, lead),
            "lead": lead,
        }
    )


@login_required
def lead_full(request, lead):
    return loader.render_to_string(
        request=request,
        template_name="hitarget/components/lead_full.html",
        context={"lead": lead, "associated_actions": lead.generate_action_buttons_maxi(request)}
    )


@login_required
def add_lead(request):
    if request.method == "POST":
        pp.pprint("Received POST data %s" % (request.POST))
        add_lead_form = AddLeadForm(data=request.POST)
        if add_lead_form.is_valid():
            print("is valid")
            new_item = add_lead_form.save(commit=False)
            new_item.author = request.user
            new_item.save()
            # redirect to newly created item
            messages.info(request, _("Votre lead est en ligne, le voici:"))
            return redirect(new_item.get_absolute_url())
        else:
            print("invalid form data")


    elif request.method == "GET":
        add_lead_form = AddLeadForm(initial=fake_lead_add_form_data())
    return render(
        request=request,
        template_name="hitarget/leads/add_or_edit.html",
        context={'add_lead_form': add_lead_form}
    )


def tips(request):
    return render(
        request=request,
        template_name="hitarget/leads/tips.html",
        context={}
    )


@login_required
def lead_edit(request, slug):
    instance = get_object_or_404(Lead, slug=slug)
    # check permission
    current_user = request.user
    print("user %s trying to change lead belonging to %s, can==%s" % (current_user, instance.author, instance.author == current_user))
    # TODO raise 403
    add_lead_form = AddLeadForm(data=request.POST or None, instance=instance)
    if add_lead_form.is_valid():
        print("edition is valid")
        add_lead_form.save()
        messages.info(request, "Lead bien mis à jour")
        return redirect(to=instance.get_absolute_url())
    return render(
        request=request,
        template_name="hitarget/leads/add_or_edit.html",
        context={'add_lead_form': add_lead_form})


def lead_delete(request, slug):
    instance = get_object_or_404(Lead, slug=slug)
    # check permission
    current_user = request.user
    print("[%s]user %s trying to delete lead belonging to %s, can==%s" % (request.method, current_user, instance.author, instance.author == current_user))
    # TODO raise 403
    if request.method == "POST":
        instance.delete()
        messages.info(request, "Votre lead est désormais supprimé")
        return redirect(to=reverse('hitarget:home'))
    else:
        return render(
            request=request,
            template_name="hitarget/leads/delete.html",
            context={"lead": instance}
        )


@login_required
def my_leads(request):
    current_user = request.user
    current_user_leads = current_user.leads.all()
    print("found %d leads for author %s:%s" % (len(current_user_leads), current_user, current_user_leads))
    return render(
        request=request,
        template_name="hitarget/leads/my-leads.html",
        context={"leads": current_user_leads}
    )
