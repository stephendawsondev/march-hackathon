from django.contrib import admin
from unfold.admin import ModelAdmin
# from import_export.admin import ImportExportModelAdmin # ImportExportModel functionality

# UPDATE THE BELOW IMPORTS WITH THE APP'S MODEL
# AND UNCOMMENT:
# from .models import OsProjectModel

# @admin.register(OsProjectModel)
# class CustomAdminClass(ModelAdmin):
#     pass

# -- OR -- THIS WITH IMPORT/EXPORT FUNCTIONALITY:

# class MyAppAdmin(ImportExportModelAdmin):
#     resource_classes = [MyAppResource]

# @admin.register(OsProjectModel, MyAppAdmin)
# class CustomAdminClass(ModelAdmin):
#     pass
