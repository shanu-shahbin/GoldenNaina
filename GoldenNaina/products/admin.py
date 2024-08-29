from django.contrib import admin
from .models import Product, Wishlist, ProductImages, ProductReview, Category, Theme_model, Size, Stock, PopularSearch


class ProductImagesInline(admin.TabularInline):
    model = ProductImages

class StockInline(admin.TabularInline):
    model = Stock
    extra = 1

class Theme_modelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'discount_price', 'in_stock', 'created_at', 'product_image', 'return_policy')
    list_filter = ('in_stock', 'created_at')
    search_fields = ('title', 'description')
    inlines = [ProductImagesInline, StockInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('stocks')

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'date')
    list_filter = ('product', 'date')
    search_fields = ('user__username', 'product__title')
    ordering = ('-date',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('product')

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'date')
    list_filter = ('date',)
    ordering = ('-date',)

class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Ensure this is a tuple

class PopularSearchAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')

admin.site.register(Product, ProductAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Theme_model, Theme_modelAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Stock)
admin.site.register(PopularSearch, PopularSearchAdmin)

