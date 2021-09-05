from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm


# Create your views here.
def get_todo_list(request):
    items = Item.objects.all()
    # context dic is the way we pas var to the template
    # The key should correspond to the var we want to pass
    context = {
        'items': items
    }
    return render(request, 'todo/todo_list.html', context)


def add_item(request):
    if request.method == 'POST':
        # Use the form template to populate the form automatically
        # with the request.post method
        form = ItemForm(request.POST)
        # Check the form validity
        if form.is_valid():
            # save the form
            form.save()  # corresp to Item.objects.create(name=name, done=done)
            return redirect('get_todo_list')

        # Get the forms info
        # name = request.POST.get('item_name')
        # done = 'done' in request.POST

        # Create an Item  in the db
        # Item.objects.create(name=name, done=done)

    form = ItemForm()
    context = {
        'form': form
    }
    return render(request, 'todo/add_item.html', context)


def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('get_todo_list')

    # the instance=item param is to tell the form to prepopulate
    # with the item retreived above
    form = ItemForm(instance=item)
    context = {
        'form': form
    }
    return render(request, 'todo/edit_item.html', context)


def toggle_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.done = not item.done
    item.save()
    return redirect('get_todo_list')


def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect('get_todo_list')
