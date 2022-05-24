from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, logout_then_login, LogoutView
from django.contrib.auth import views as auth_views
from hospital import views as user_views

urlpatterns = [
    path('administrator/', admin.site.urls),
    path('',include('hospital.urls')),
    # path(r'^accounts/', include('registration.backends.simple.urls')),
    path('8f6yyE*!Hc7mtgBpw@$wpT31*1pGFh&puajjYKqoWgidA!Xk59ju8lw7geiSCNlnStUWrLm!v7Y2J@9oFS2upRnZN34TsMl3I9XMLRctqmcpeb28UYIRk!9$$m!k0h6K3mW2!YcHSUXkH2H6*Fhzc5smR4@z@ttlQSHx*$*Qcs4f6k@h7N4pCWLED2Nhpjw0JJVmcfwx/', auth_views.LoginView.as_view(template_name='user/login.html'), name = 'login'),
    path('uM64cT$afW!K7lFxLgaPFiLLMoM&OqtDIuk6FEX!VmOo!XFRgb1xCOxTK7gnHvD0OTjUKTjGW2uGRj3CJxniuFNs$AAMhq*yCZFkvt*18cei4uxP1omiYZH0NGeP8Z0pnaw3HaODFEs!$6g6FFbRfcZFe$RKnaqroYXJwc&6!vPzI2RbD!isHFniLOs@OYW@JtzQyPd4/', user_views.registration_view, name = 'registration'),
    path('ojblGw77xxibHduy53rWvSOxRR1zPfxW9n$!QnFdYGmPcGe$*CbnL!0FPMWuE*@jPX4dxjbaL1AcQprzmHpUyLrZYUHU27nkVCbFS6Z7fHrGVDLZqlQikaR1coieuj$MH0VFMEKKGIh@O$lfVj0opra!kl$xjaiaINmemUR7Fx5hC4Q8nrsXbqNAjXysJtF8J3PxxZVG/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name = 'password_reset'),
    path('N7azqG!*Xt5Sf9SbiDBU$hw8X@CODET75V2f4bWW7E1DobugrGmIhCu5x8AHYi80Le8qBGH9t6W736ZCyzF!rrOsrZxT3Dx6VQuCO16@mdc2s1COydofGjlsRuOrt8cyStJS7n@l0z0OuEMP8Mf5jxeOzr0NYG&&iL$JzVUlhYfKHckr2Ip4QtdKtwuqr!I8K&QCurLE/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name = 'password_reset_done'),
    path('Rz6e6BiZu*nf2ikVvoM7rH&3FHVJljPBxDWoTbENAg4EhQb8b961x!xTiub*GE9eqsm!bpDvHjvC*AW0fRDjrzxJKsubdrjwW9OY9n1Fyki8Q@VNOR64NQKV8zZdRwxOHpqFA5ygjSvk904AtOR8$AOPAkFhImhb@Nwr2oqACCu!wpmuPER!b4YqMEa0blmKlBKnGSor/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name = 'password_reset_confirm'),
    path('bIyuZq7j2ja@78Zc*LMU&chNwH1VCllZqsq4o$ln5PLcqooaCYbNfwMyqngFr$u5Rb4u2d810APex9uqhbSGfLumsS4qZkQaN3rNw74Ke@gal!d03daT!I551$PegceDUGEc$XtAXhpKtrIxPnUew60yrDP2*jyNcDRubeyJgU16M2*Hippz@VLIcGd4UuiJ3nRoLKmr/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name = 'password_reset_complete'),
    
    path('logout/', LogoutView.as_view(), name='logout'), 
]
