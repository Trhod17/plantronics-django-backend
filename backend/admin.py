from django.contrib import admin
from backend.models import (Plant,
                            Family,
                            Info,
                            SoilPreference,
                            UserPlant,
                            Genus,
                            Edible)


class InfoInline(admin.StackedInline):
    model = Info
    extra = 1


class SoilPreferenceInline(admin.StackedInline):
    model = SoilPreference
    extra = 1


class PlantAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": [
                'plant_name', 'plant_latin_name', 'plant_image', 'plant_description',
                'family', 'genus', 'created_by'
            ]
        }),
    )
    list_display = ('plant_name', 'plant_latin_name',
                    'plant_description', 'family', 'genus', 'created_by')
    list_filter = ('plant_name', 'plant_latin_name',
                   'plant_description', 'family', 'genus', 'created_by')
    inlines = [InfoInline, SoilPreferenceInline]


class FamilyAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": [
                'family', 'family_description', 'created_by'
            ]
        }),
    )

    list_display = ('family', 'family_description', 'created_by')


class GenusAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": [
                'genus', 'genus_description', 'created_by'
            ]
        }),
    )

    list_display = ('genus', 'genus_description', 'created_by')


class SoilPreferenceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": [
                'plants', 'preference', 'soil_description', 'created_by'
            ]
        }),
    )

    list_display = ('plants', 'preference', 'soil_description', 'created_by')


class UserPlantAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": [
                'username', 'user', 'plant'
            ]
        }),
    )

    list_filter = ('username', 'user', 'plant')


class InfoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": [
                'plant', 'season', 'time_frame',
                'sun_preference', 'climate', 'info_description', 'created_by'
            ]
        }),
    )
    list_display = ('plant', 'season', 'time_frame',
                    'sun_preference', 'climate', 'info_description', 'created_by')
    list_filter = ('plant', 'season', 'time_frame',
                   'sun_preference', 'climate', 'info_description', 'created_by')


class EdibleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": [
                'plant', 'is_fruit_edible', 'fruit_image', 'are_leaves_edible',
                'leaf_image', 'are_roots_edible', 'root_image', 'are_flowers_edible',
                'flower_image', 'are_seeds_edible', 'seed_image', 'edible_description', 'created_by',

            ]
        }),
    )

    list_display = ('plant', 'is_fruit_edible', 'are_leaves_edible',
                    'are_roots_edible', 'are_flowers_edible',
                    'are_seeds_edible', 'edible_description', 'created_by')

    list_filter = ('plant', 'is_fruit_edible', 'are_leaves_edible',
                   'are_roots_edible', 'are_flowers_edible',
                   'are_seeds_edible', 'created_by')


admin.site.register(Family, FamilyAdmin)
admin.site.register(Plant, PlantAdmin)
admin.site.register(Info, InfoAdmin)
admin.site.register(SoilPreference, SoilPreferenceAdmin)
admin.site.register(UserPlant, UserPlantAdmin)
admin.site.register(Genus, GenusAdmin)
admin.site.register(Edible, EdibleAdmin)
