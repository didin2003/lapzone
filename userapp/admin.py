from django.contrib import admin
from . models import Reg_tbl,Pro_tbl,Rent_tbl,cart_tbl,sell_tbl,service_tbl,rental_tbl,sell_pro_tbl,customer_tbl

admin . site .register(Reg_tbl)
admin . site .register(Pro_tbl)
admin . site .register(Rent_tbl)
admin . site . register(cart_tbl)
admin . site . register(sell_tbl)
admin . site . register(service_tbl)
admin . site . register(rental_tbl)
admin . site . register(sell_pro_tbl)
admin . site . register(customer_tbl)

