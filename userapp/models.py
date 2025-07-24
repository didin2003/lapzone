from django.db import models

class Reg_tbl(models.Model):
    fname = models.CharField(max_length=25)
    mobile = models.IntegerField()
    email = models.EmailField()
    pssw = models.CharField(max_length=16)
    cpssw = models.CharField(max_length=16)
    add   = models.TextField(default='not entered')
    pincode  = models.IntegerField(default=0)
    

class Pro_tbl(models.Model):
    pnm = models.CharField(max_length=25)
    prc = models.IntegerField()
    pim = models.ImageField(upload_to='pic')
    des = models.TextField()
    

class Rent_tbl(models.Model):
    rpnm = models.CharField(max_length=30)
    rprc = models.IntegerField()
    rpim = models.ImageField(upload_to='rpic')
    rdes = models.TextField()

class cart_tbl(models.Model):
    product = models.ForeignKey(Pro_tbl,on_delete=models.CASCADE)
    customer = models.ForeignKey(Reg_tbl,on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)


class sell_tbl(models.Model):
    sname = models.CharField(max_length=25)
    smobile = models.IntegerField()
    semail = models.EmailField()
    spssw = models.CharField(max_length=16)
    scpssw = models.CharField(max_length=16)
    
class service_tbl(models.Model):
    name = models.CharField (max_length=25,default='unknown')
    item = models.CharField(max_length=30)
    issues = models.TextField()
    address = models.TextField()
    mobile = models.IntegerField()
    date = models.DateField()


class rental_tbl(models.Model):
    rname = models.CharField(max_length=50, default='Unknown') 
    raddress = models.TextField()
    raadhar = models.BigIntegerField()  
    rmobile = models.BigIntegerField()  
    rdate = models.DateField()
    rmonths = models.IntegerField()  
    ramount = models.IntegerField(default=0)  
    ritem  = models.CharField(max_length=80 , default='item')
    rprice = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.rname} - {self.rmonths} months (Rs {self.ramount})"

class sell_pro_tbl(models.Model):
    products = models.ForeignKey(Pro_tbl,on_delete=models.CASCADE)
    seller   = models.ForeignKey(sell_tbl,on_delete=models.CASCADE)


class customer_tbl(models.Model):
    product = models.ForeignKey(Pro_tbl,on_delete=models.CASCADE)
    user = models.ForeignKey(Reg_tbl,on_delete=models.CASCADE)