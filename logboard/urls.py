from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^$', 'logboard.views.index'),
	(r'^reset/$', 'logboard.views.reset'),
	(r'^connected$', 'logboard.views.connected'),
	(r'^disconnected$', 'logboard.views.disconnected'),
	(r'^message$', 'logboard.views.message'),
	(r'^test/$', 'logboard.views.test'),
	(r'^broadcast/$', 'logboard.views.broadcast'),
)

