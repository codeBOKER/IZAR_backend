# Generated by Django 5.0.1 on 2025-07-13 08:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_category_imgur_url_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'تصنيف', 'verbose_name_plural': 'تصنيفات'},
        ),
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(verbose_name='الوصف'),
        ),
        migrations.AlterField(
            model_name='category',
            name='header',
            field=models.CharField(max_length=100, verbose_name='العنوان'),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.URLField(blank=True, null=True, verbose_name='الصورة'),
        ),
        migrations.AlterField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='نشط'),
        ),
        migrations.AlterField(
            model_name='category',
            name='sizes',
            field=models.TextField(blank=True, help_text='قائمة المقاسات المتوفرة مفصولة بفواصل (مثال: S,M,L,XL)', verbose_name='المقاسات'),
        ),
        migrations.AlterField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث'),
        ),
        migrations.AlterField(
            model_name='email',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإرسال'),
        ),
        migrations.AlterField(
            model_name='email',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='البريد الإلكتروني'),
        ),
        migrations.AlterField(
            model_name='email',
            name='message',
            field=models.TextField(verbose_name='الرسالة'),
        ),
        migrations.AlterField(
            model_name='email',
            name='name',
            field=models.CharField(max_length=100, verbose_name='الاسم'),
        ),
        migrations.AlterField(
            model_name='email',
            name='phone_number',
            field=models.CharField(max_length=20, verbose_name='رقم الهاتف'),
        ),
        migrations.AlterField(
            model_name='email',
            name='topic',
            field=models.CharField(max_length=200, verbose_name='الموضوع'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='core.category', verbose_name='التصنيف'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='الوصف'),
        ),
        migrations.AlterField(
            model_name='product',
            name='header',
            field=models.CharField(max_length=200, verbose_name='العنوان'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='نشط'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='السعر'),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث'),
        ),
        migrations.AlterField(
            model_name='productcolor',
            name='color_code',
            field=models.CharField(editable=False, max_length=7, verbose_name='كود اللون'),
        ),
        migrations.AlterField(
            model_name='productcolor',
            name='image',
            field=models.URLField(blank=True, null=True, verbose_name='الصورة'),
        ),
        migrations.AlterField(
            model_name='productcolor',
            name='is_available',
            field=models.BooleanField(default=True, verbose_name='متوفر'),
        ),
        migrations.AlterField(
            model_name='productcolor',
            name='name',
            field=models.CharField(choices=[('FF0000', 'أحمر'), ('0000FF', 'أزرق'), ('008000', 'أخضر'), ('FFFF00', 'أصفر'), ('FFA500', 'برتقالي'), ('800080', 'بنفسجي'), ('FFC0CB', 'وردي'), ('A52A2A', 'بني'), ('000000', 'أسود'), ('FFFFFF', 'أبيض')], help_text='اختر لونًا', max_length=50, verbose_name='اللون'),
        ),
        migrations.AlterField(
            model_name='productcolor',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colors', to='core.product', verbose_name='المنتج'),
        ),
        migrations.AlterField(
            model_name='review',
            name='feedback',
            field=models.TextField(verbose_name='الملاحظات'),
        ),
        migrations.AlterField(
            model_name='review',
            name='image',
            field=models.URLField(blank=True, null=True, verbose_name='الصورة'),
        ),
        migrations.AlterField(
            model_name='review',
            name='job_description',
            field=models.CharField(max_length=100, verbose_name='المسمى الوظيفي'),
        ),
        migrations.AlterField(
            model_name='review',
            name='name',
            field=models.CharField(max_length=100, verbose_name='الاسم'),
        ),
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='التقييم'),
        ),
        migrations.AlterField(
            model_name='review',
            name='view',
            field=models.BooleanField(default=False, verbose_name='مرئي'),
        ),
    ]
