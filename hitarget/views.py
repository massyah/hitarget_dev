from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
import pprint as pp
from .models import Lead
from .forms import AddLeadForm


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
        context={"lead": lead}
    )
    return ff


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


def lead_maxi(request, lead):
    return loader.render_to_string(
        request=request,
        template_name="hitarget/components/lead_maxi.html",
        context={"lead": lead}
    )


def lead_detail_full(request, slug):
    # TODO add check that lead is actually bought
    print("getting %s",slug)
    lead = get_object_or_404(Lead, slug=slug)
    return render(
        request=request,
        template_name="hitarget/leads/detail_full.html",
        context={
            "lead_html": lead_full(request, lead),
            "lead": lead,
        }
    )


def lead_full(request, lead):
    return loader.render_to_string(
        request=request,
        template_name="hitarget/components/lead_full.html",
        context={"lead": lead}
    )


def add_lead(request):
    if request.method == "POST":
        pp.pprint("Received POST data %s"%(request.POST))
        add_lead_form = AddLeadForm(data=request.POST)
        if add_lead_form.is_valid():
            print("is valid")
            new_item = add_lead_form.save(commit=True)
            # redirect to newly created item
            return redirect(new_item.get_absolute_url())
        else:
            print("invalid form data")


    elif request.method == "GET":
        add_lead_form = AddLeadForm()
    return render(
        request=request,
        template_name="hitarget/leads/add.html",
        context={'add_lead_form': add_lead_form}
    )

def tips(request):
    return render(
        request=request,
        template_name="hitarget/leads/tips.html",
        context={}
    )