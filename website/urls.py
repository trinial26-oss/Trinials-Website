from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    # Primary Pages
    path('', views.home, name='home'),
    path('about/', views.about_page, name='about_page'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.terms_conditions, name='terms_conditions'),
    path('design-preview/', views.design_preview, name='design_preview'),
    path('contact/', views.contact_submit, name='contact'),

    # Technical SEO Endpoints
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    path('robots.txt', views.robots_txt, name='robots_txt'),

    # SEO Service Landing Pages
    path('services/', views.services_index, name='services_index'),
    path('services/web-development/', views.service_web_development, name='service_web_development'),
    path('services/ui-ux-design/', views.service_ui_ux_design, name='service_ui_ux_design'),
    path('services/ecommerce-development/', views.service_ecommerce_development, name='service_ecommerce_development'),
    path('services/custom-software-development/', views.service_custom_software_development, name='service_custom_software_development'),
    path('services/brand-identity-design/', views.service_brand_identity_design, name='service_brand_identity_design'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),

    # SEO Insights / Customer Knowledge Guides
    path('insights/', views.insights_index, name='insights_index'),
    path('insights/website-development-cost-in-kerala/', views.insight_website_cost, name='insight_website_cost'),
    path('insights/why-businesses-need-professional-website/', views.insight_why_need_website, name='insight_why_need_website'),
    path('insights/custom-website-vs-wordpress/', views.insight_custom_vs_wordpress, name='insight_custom_vs_wordpress'),
    path('insights/ecommerce-website-development-guide/', views.insight_ecommerce_guide, name='insight_ecommerce_guide'),
    path('insights/how-to-choose-web-development-company-kerala/', views.insight_choose_company, name='insight_choose_company'),
    path('insights/<slug:slug>/', views.insight_detail, name='insight_detail'),
]
