"""管理员相关接口路由"""
from django.urls import path

import software_app.implement.admin_imple as admin_imple


urlpatterns = [
    path('update-pile', admin_imple.update_pile_api),
    path('query-report', admin_imple.query_report_api),
    path('query-all-piles_stat', admin_imple.query_all_piles_stat_api),
    path('query-queue', admin_imple.query_queue_api),
]
