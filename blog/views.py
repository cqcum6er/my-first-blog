from django.shortcuts import render

def post_list(request):
    return render(request, 'blog/post_list.html', {})  #To serve as a template, 'blog/post_list.html' has to be put in blog\template\blog\