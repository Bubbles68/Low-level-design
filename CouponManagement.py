
'''Entities:
users: list of coupons, list of voucher, user id, user name
coupons: expiry_date, status
vouchers: expiry_date, status, userId
Manager: createCoupon, deleteCoupon, activate/deactivate coupons
'''
from enum import Enum


class Status(Enum):
    ACTIVATED = 0
    DEACTIVATED = 1

class User:
    def __init__(self, name, userId, cartValue, age):
        self._name = name
        self._userId = userId
        self.couponList = []
        self.cartValue = cartValue
        self.age = age
        
    def get_name(self):
        return self._name
    
    def get_userId(self):
        return self._userId
        
class Coupon:
    def __init__(self, couponId, expiryDate, totalLimit, minCartValue, minAge):
        self.couponId = couponId
        self.expiryDate = expiryDate
        self.status = Status.DEACTIVATED
        self.limit = totalLimit
        self.minCartValue = minCartValue
        self.minAge = minAge
        self.uses = 0
        
class Manager:
    def __init__(self):
        self.coupons = {}
        self.users = {}
        
    def createCoupon(self, couponExpiryDate, totalLimit, minAge, minCartValue):
        couponId = "c-"+str(len(self.coupons))
        coupon = Coupon(couponId, couponExpiryDate, totalLimit, minCartValue, minAge)
        self.coupons[couponId] = coupon
        
        
    def activateCoupon(self, coupon):
        self.coupons[coupon.couponId].self.status = Status.ACTIVATED
        
    def applyCoupon(self, couponId, userId): 
        if user.userId not in self.users or couponId not in self.coupons:
            return False
        
        user = self.users[userId]
        coupon = self.coupons[couponId]
        
        if coupon.status==Status.ACTIVATED and coupon.uses<coupon.totalLimit and user.cartValue>=coupon.minCartValue and user.age>=coupon.minAge:
            coupon.uses+=1
            user.couponList.append(coupon)
            return True
        return False
        
        