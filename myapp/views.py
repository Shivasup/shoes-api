from django.views import View
from django.http import JsonResponse
from .models import Shoe


class ShoeView(View):
    def get(self, request):
        shoes = Shoe.objects.all()

        # 🔹 Query params
        category = request.GET.get('category')
        search = request.GET.get('search')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        rating = request.GET.get('rating')
        brand = request.GET.get('brand')
        color = request.GET.get('color')
        sort = request.GET.get('sort')

        # 🔍 Filters
        if category:
            shoes = shoes.filter(category__iexact=category)

        if search:
            shoes = shoes.filter(name__icontains=search)

        if brand:
            shoes = shoes.filter(brand__iexact=brand)

        if color:
            shoes = shoes.filter(color__iexact=color)

        if min_price:
            try:
                shoes = shoes.filter(price__gte=int(min_price))
            except:
                pass

        if max_price:
            try:
                shoes = shoes.filter(price__lte=int(max_price))
            except:
                pass

        if rating:
            try:
                shoes = shoes.filter(rating__gte=float(rating))
            except:
                pass

        # 🔽 Sorting
        if sort == 'low':
            shoes = shoes.order_by('price')
        elif sort == 'high':
            shoes = shoes.order_by('-price')
        elif sort == 'rating':
            shoes = shoes.order_by('-rating')

        # 📄 Pagination
        try:
            page = int(request.GET.get('page', 1))
            limit = int(request.GET.get('limit', 5))
        except:
            page = 1
            limit = 5

        start = (page - 1) * limit
        end = start + limit

        total = shoes.count()
        shoes = shoes[start:end]

        # 📦 Output
        data = []
        for shoe in shoes:
            image_url = request.build_absolute_uri(shoe.image.url) if shoe.image else None

            data.append({
                "id": shoe.id,
                "name": shoe.name,
                "brand": shoe.brand,
                "price": shoe.price,
                "category": shoe.category,
                "rating": shoe.rating,
                "color": shoe.color,
                "size": shoe.size,
                "image": image_url
            })

        return JsonResponse({
            "total": total,
            "page": page,
            "limit": limit,
            "results": data
        })