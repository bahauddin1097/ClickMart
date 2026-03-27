from django.conf import settings
from django.core.mail import send_mail

def send_order_notification(order):
    send_mail(
        subject=f'Order #{order.id} is received',
        message=f'''
            Hi {order.user.first_name},

            Your order with Order ID: #{order.id} has been placed successfully.
            Total: {order.grand_total}

            Thank you for shopping with us.
        ''',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[order.user.email,],
        fail_silently=False,
    )
    return