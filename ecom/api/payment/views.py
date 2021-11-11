from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

import braintree
# Create your views here.

import braintree

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="fmtw4prfcptg69sb",
        public_key="fq9y6jzftqh89sr7",
        private_key="d7cde97c7e91c2426bd5af40183af43"
    )
)

def validate_user_session(id, token):
    UserModel= get_user_model()

    try:
        user=UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False
    except UserModel.DoesnotExist:
            return False


@csrf_exempt
def generate_token(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error':'Invalid session, please login again'})
    return JsonResponse({'clientToken':gateway.client_token.generate(),'success':True})


@csrf_exempt
def process_payment(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error':'Invalid session, please login again'})
    
    nonce_from_the_client=request.POST["paymentMethodNonce"]
    amount_from_the_client= request.POST["amount"]

    result= gateway.transaction.sale({
        "amount":amount_from_the_client,
        "payment_method_nonce":nonce_from_the_client,
        "options":{
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        return JsonResponse({
            "success":result.is_success,'transaction':{'id': result.transaction.id,'amount':result.transaction.amount}})
    else:
        return JsonResponse({'error': True, 'success': False})