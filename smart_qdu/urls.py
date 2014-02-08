from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smart_qdu.views.home', name='home'),
    # url(r'^smart_qdu/', include('smart_qdu.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'smart_qdu.views.index'),
    url(r'^500/$', 'smart_qdu.views.server_error'),

    url(r'^login/$', 'Account.views.log_in'),
    url(r'^logout/$', 'Account.views.logout'),
    url(r'^register/$', 'Account.views.register'),
    url(r'^change_password/$', 'Account.views.change_password'),
    url(r'^user_profile/$', 'Account.views.user_profile'),

    url(r"^classroom/$", "EmptyClassroom.views.query_empty_classroom_web"),
    url(r'^import_classroom_info', 'EmptyClassroom.views.import_classroom_info'),

    url(r"^lost_and_found/$", 'LostAndFound.views.index_page'),
    url(r'^lost_and_found/post_info/(?P<info_type>\w+)/$', 'LostAndFound.views.post_info'),
    url(r'^lost_and_found/info/(?P<info_id>\d+)/$', 'LostAndFound.views.show_info_detail'),
    url(r'^lost_and_found/info/(?P<info_id>\d+)/post_comment/$', 'LostAndFound.views.post_comment'),
    url(r'^lost_and_found/info/(?P<info_id>\d+)/mark/$', 'LostAndFound.views.mark_item_status'),
    url(r'^lost_and_found/info_list/(?P<page_num>\d+)/$', 'LostAndFound.views.show_info_list'),

    url(r'^weixin/$', 'Weixin.views.weixin_main'),
    url(r'^weixin/access_token/$', 'Weixin.views.access_token'),

    url(r'^online_shop/$', 'OnlineShop.views.shop_index'),
    url(r'^online_shop/item/(?P<item_id>\d+)/$', 'OnlineShop.views.item_page'),
    url(r'^online_shop/item/(?P<item_id>\d+)/create_order/$', 'OnlineShop.views.create_order'),
    url(r'^online_shop/item/(?P<item_id>\d+)/submit_order/num/(?P<number>\d+)/$', 'OnlineShop.views.submit_order'),
    url(r'^online_shop/order/(?P<order_id>\d+)/$', 'OnlineShop.views.order_info'),
    url(r'^online_shop/item/(?P<item_id>\d+)/submit_order/num/(?P<number>\d+)/$', 'OnlineShop.views.submit_order'),

    url(r'^score/$', "Weixin.get_score.get_score"),
    url(r'^bind_jw/(?P<weixin_id>.+)/$', 'Weixin.bind_jw.bind_jw'),
    url(r'^unbind_jw/(?P<weixin_id>.+)/$', 'Weixin.bind_jw.unbind_jw'),

    url(r'renren/$', 'Renren.views.renren_oauth'),
    url(r'renren_callback/$', 'Renren.views.get_access_token'),
    url(r'renren_test/$', 'Renren.views.post_test'),

    url(r'^vote/(?P<vote_id>\d+)/(?P<weixin_id>.+)/$', 'Vote.views.vote'),
  )