from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Review, Product
from .serializers import ReviewSerializer, ProductSerializer,CategorySerializer, EmailSerializer
from rest_framework.pagination import PageNumberPagination
from django.core.mail import send_mail
from django.conf import settings



@api_view(['GET',])
def last_two_categories_with_products_view(request):
    categories = Category.objects.order_by('-created_at')[:2]
    products_category_one = Product.objects.filter(category=categories[0]).order_by('-created_at')[:2]
    products_category_two = Product.objects.filter(category=categories[1]).order_by('-created_at')[:2]

    category_one_serializer = CategorySerializer(categories[0])
    products_one_serializer = ProductSerializer(products_category_one, many=True)
    category_two_serializer = CategorySerializer(categories[1])
    products_two_serializer = ProductSerializer(products_category_two, many=True)

    return Response({'categories': [
        {
            'category': category_one_serializer.data,
            'products': products_one_serializer.data
        },
        {
            'category': category_two_serializer.data,
            'products': products_two_serializer.data
        }
    ]}, status=status.HTTP_200_OK)

@api_view(['GET',])
def review_view(request):
    reviews = Review.objects.filter(view=True)[:4]
    serializer=ReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET',])
def category_products_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({"detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    products = Product.objects.filter(category=category).order_by('-created_at')

    paginator = PageNumberPagination()
    paginated_products = paginator.paginate_queryset(products, request)

    serializer_product= ProductSerializer(paginated_products, many=True)
    serializer_category= CategorySerializer(category)
    
    return Response({
        'category': serializer_category.data,
        'products': serializer_product.data,
    }, status=status.HTTP_200_OK)

@api_view(['GET',])
def product_view(request):
    products = Product.objects.all()
    paginator = PageNumberPagination()
    paginated_products = paginator.paginate_queryset(products, request)
    serializer=ProductSerializer(paginated_products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST',])
def email_view(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        name = serializer.validated_data['name']
        email = serializer.validated_data['email']
        phone= serializer.validated_data['phone_number']
        message = serializer.validated_data['message']
        topic = serializer.validated_data['topic']

        # send the email
        send_mail(
            subject=f"New message from {name}: ({phone})",
            message=f"{topic}\n{message}",
            from_email=email,  
            recipient_list=settings.EMAILS,
            fail_silently=False,
        )

        return Response(
            {'message': 'Email sent successfully!'},
            status=status.HTTP_200_OK
        )

    return Response(
        {"details":serializer.errors,"faild_data":request.data},
        status=status.HTTP_400_BAD_REQUEST
    )


