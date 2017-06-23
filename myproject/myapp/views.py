# -*- coding: utf-8 -*-
import sys
import subprocess
import re

from django.shortcuts import render_to_response
# from django.utils import simplejson
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from PIL import Image
import random, string
from django.shortcuts import render
from django.template import loader
from django.shortcuts import redirect

from django.utils import timezone

from ipware.ip import get_ip

from random import randint

from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image
#from settings import project_ROOT #to import "os"
import os

from django.core.urlresolvers import resolve
from myproject.myapp.models import Document, Piece, Banned, Deletion
from myproject.myapp.forms import DocumentForm

from django.conf import settings 
import datetime
from django.db import models

def folder_size_cmd():
    cmd = ["du", "-sh", "-b", "/home/adefrutoscasado/MOSAICS/media"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    total = str(proc.stdout.read())
    total = re.findall('\d+', total)[0]
    return total

    
def registerdeletion(documenttodelete):
    deletion = Deletion()
    deletion.identifier = documenttodelete.identifier
    deletion.owner = documenttodelete.owner
    deletion.created_date = documenttodelete.created_date
    deletion.deletion_date = timezone.now()
    
    deletion.time_of_life = deletion.deletion_date - deletion.created_date 
    
    pieces = Piece.objects.filter(documentidentifier__exact = documenttodelete.identifier)
    
    number_of_pieces = str(int(documenttodelete.divx) * int(documenttodelete.divy))
    
    deletion.number_of_pieces = number_of_pieces

    number_of_pieces_in_db = len(pieces)

    number_of_given = len(pieces.filter(state__exact = "given"))
    number_of_submited = len(pieces.filter(state__exact = "submited"))
    number_of_accepted = len(pieces.filter(state__exact = "accepted"))
    
    deletion.pieces_given = int(number_of_given)/int(number_of_pieces)
    deletion.pieces_submited = int(number_of_submited)/int(number_of_pieces)
    deletion.pieces_accepted = int(number_of_accepted)/int(number_of_pieces)
    deletion.pieces_unused = (int(number_of_pieces) - int(number_of_pieces_in_db)) / int(number_of_pieces)
    
    deletion.save()
    
    return None
    

def folder_size(path):
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += folder_size(entry.path)
    return total


def check_limit_storage():
    #limit_to_start_removing = 2097152 #around 2 mb, debug
    limit_to_start_removing = 419430400 #400 mb
    
    path = "/home/alejandro/Desktop/mosaics/MOSAICS/media" #for local Linux
    #path = "/home/adefrutoscasado/MOSAICS/media" #para pythonanywhere
    #path = "media" #for windows
    
    used_storage = folder_size(path)
    if int(str(used_storage)) > int(str(limit_to_start_removing)):
        Oldest_document = Document.objects.earliest('created_date')
        identifier = Oldest_document.identifier
        registerdeletion(Oldest_document);
        Oldest_document.delete()
        Pieces_oldest_documents = Piece.objects.filter(documentidentifier__exact = identifier)
        Pieces_oldest_documents.delete()
        Banneds_oldest_documents = Banned.objects.filter(documentidentifier__exact = identifier)
        Banneds_oldest_documents.delete()
        check_limit_storage() #we call the function until we use only 400 mb
    return None;

def listofprojects(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            format = Image.open(newdoc.docfile).format
            if format != "JPEG":
                if format != "PNG":
                    template = loader.get_template('infomessage.html')
                    context = {'message': 'Format not allowed! Please use JPG or PNG'}
                    return HttpResponse(template.render(context, request))

            check_limit_storage() #check if there is enough available storage
            
            if form.check_file_size() == "false":
                template = loader.get_template('infomessage.html')
                context = {'message': 'The size of the image should be less than 2 Mb'}
                return HttpResponse(template.render(context, request))
            
            newdoc.mosaic = request.FILES['docfile']
            
            if newdoc.image_height < 50:
                template = loader.get_template('infomessage.html')
                context = {'message': 'The size of the image should be more than 50x50 pixels'}
                return HttpResponse(template.render(context, request))
            if newdoc.image_width < 50:
                template = loader.get_template('infomessage.html')
                context = {'message': 'The size of the image should be more than 50x50 pixels'}
                return HttpResponse(template.render(context, request))
            
            newdoc.identifier = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8)) #we add the identifier
            newdoc.owner = request.COOKIES['user']
            newdoc.save()

            # Redirect to the admin page after POST
            documents = Document.objects.get(pk=newdoc.id)
            template = loader.get_template('conf.html')
            context = {'documents': documents, 'form': form}

            #Debug the manage of size
            #tamano = folder_size("/media")
            #return HttpResponse(str(tamano))

            return HttpResponse(template.render(context, request))
        else:
            template = loader.get_template('infomessage.html')
            context = {'message': 'Captcha error. Try again.'}
            return HttpResponse(template.render(context, request))

    else:
        
        id_user = "null"
        known_user = "true"
        if ('user') not in request.COOKIES:
            id_user =  ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(30))
            known_user = "false"
        else:
            id_user = request.COOKIES['user']

        form = DocumentForm()  # A empty, unbound form

        documents = Document.objects.filter(owner__exact=id_user) #primero leemos para eliminar viejos

        for document in documents: #If the project was aborted while choosing the divs, it will be deleted
            if document.divx is None:
                identifier = document.identifier
                document.delete()
                Pieces_oldest_documents = Piece.objects.filter(documentidentifier__exact = identifier)
                Pieces_oldest_documents.delete()
                Banneds_oldest_documents = Banned.objects.filter(documentidentifier__exact = identifier)
                Banneds_oldest_documents.delete()

        #return HttpResponse("he entrado donde deberia eliminar las cosas")

        documents = Document.objects.filter(owner__exact=id_user) #segunda vez que leemos, esta vez para mostrar
        
        pieces = Piece.objects.filter(owner__exact=id_user)
        
        documentsparticipate = []
        for piece in pieces:
            Documentofpiece = Document.objects.filter(identifier__exact=piece.documentidentifier)
            if Documentofpiece[0].owner != piece.owner:
                documentsparticipate.extend(Document.objects.filter(identifier__exact=piece.documentidentifier))


        template = loader.get_template('list.html')
        context = {'documents': documents, 'form': form, 'documentsparticipate': documentsparticipate}

        response = HttpResponse(template.render(context, request))
        if known_user == "false":
            response.set_cookie(key='user', value=id_user, max_age=63072000)
        
        return response


def configuration(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm()  # A empty, unbound form
        id=request.POST.get('id')
        object = Document.objects.get(pk=id)
        #docidentifier = Document.objects.get(pk=id)

        divx = request.POST.get('divx')
        divy = request.POST.get('divy')

        pieces = Piece.objects.filter(documentidentifier__exact=object.identifier) #Check if the pieces have been created before (if you go back from admin.html, and choose other division)

        if object.divx != None:
            template = loader.get_template('infomessage.html')
            context = {'message': 'You cannot change this configuration again'}
            return HttpResponse(template.render(context, request))
        
        if int(divx) > 25:
            template = loader.get_template('infomessage.html')
            context = {'message': 'Divisions sould be between 1 and 25'}
            return HttpResponse(template.render(context, request))
        if int(divx) < 1:
            template = loader.get_template('infomessage.html')
            context = {'message': 'Divisions sould be between 1 and 25'}
            return HttpResponse(template.render(context, request))
        if int(divy) > 25:
            template = loader.get_template('infomessage.html')
            context = {'message': 'Divisions sould be between 1 and 25'}
            return HttpResponse(template.render(context, request))
        if int(divy) < 1:
            template = loader.get_template('infomessage.html')
            context = {'message': 'Divisions sould be between 1 and 25'}
            return HttpResponse(template.render(context, request))

        object.divy = request.POST.get('divy')
        object.divx = request.POST.get('divx')


        documentidentifier = object.identifier
        
        object.save()
        documents = Document.objects.filter(id__exact=id)
        
        #creamos los modelos que usaremos para las piezas

        #for i in range(int(divx)):
        #        for j in range(int(divy)):
        #                newpiece = Piece()
        #                newpiece.xposition = i
        #                newpiece.yposition = j
        #                newpiece.documentidentifier = documentidentifier
        #                newpiece.identifier = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(15)) #we add the identifier
        #                newpiece.save()

    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
        documents = Document.objects.filter(id__exact=newdoc.id)

    return redirect('/project/' + documentidentifier + '/')

def thread(request, thread_id): #si recibe el thread_id. se puede usar
    if ('user') in request.COOKIES:
        user_id = request.COOKIES['user']
        
        documentswithcookie = Document.objects.filter(owner__exact=user_id).filter(identifier__exact=thread_id)

        if len(documentswithcookie) > 0: #Si el thread que se pide tiene como owner el id de la cookie del usuario, entonces muestra el modo Admin
            documentswithcookie = Document.objects.filter(identifier=thread_id)
            form = DocumentForm()
            acceptedpieces = Piece.objects.filter(documentidentifier__exact=thread_id).filter(state__exact="accepted")
            givenpieces = Piece.objects.filter(documentidentifier__exact=thread_id).filter(state__exact="given")
            submitedpieces = Piece.objects.filter(documentidentifier__exact=thread_id).filter(state__exact="submited")
            
            banneds = Banned.objects.filter(documentidentifier__exact=thread_id)
            template = loader.get_template('admin.html')
            context = {'documents': documentswithcookie, 'form': form, 'acceptedpieces': acceptedpieces, 'givenpieces': givenpieces, 'submitedpieces': submitedpieces, 'banneds': banneds}
            response = HttpResponse(template.render(context, request))
            response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate' 
            response['Expires'] = 'Fri, 01 Jan 2010 00:00:00 GMT'
            return response
        
        else: # no es admin, pero si tiene cookie 
            
            documents = Document.objects.filter(identifier__exact=thread_id)
            
            if len(documents) == 0:
                template = loader.get_template('infomessage.html')
                context = {'message': 'This mosaic doesnt exist!'}
                return HttpResponse(template.render(context, request))
            else:
                form = DocumentForm()
                template = loader.get_template('collaborator.html')
                context = {'documents': documents, 'form': form}
                response = HttpResponse(template.render(context, request))
                response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate' 
                response['Expires'] = 'Fri, 01 Jan 2010 00:00:00 GMT'
                return response

    else: # no tiene cookie, le damos una
        documents = Document.objects.filter(identifier__exact=thread_id)
        if len(documents) == 0:
            template = loader.get_template('infomessage.html')
            context = {'message': 'This mosaic doesnt exist!'}
            return HttpResponse(template.render(context, request))
        else:
            form = DocumentForm()
            template = loader.get_template('collaborator.html')
            context = {'documents': documents, 'form': form}
            response = HttpResponse(template.render(context, request))
            response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate' 
            response['Expires'] = 'Fri, 01 Jan 2010 00:00:00 GMT'
            id_user =  ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(30))
            response.set_cookie(key='user', value=id_user, max_age=63072000)
            return response
             #insertar cookie tambiennnnnnnnnnnnnnnn


def givemepiece(request):

    if request.method == 'POST':

        id = request.POST.get('id')
        object = Document.objects.get(pk=id)
        #return HttpResponse(get_ip(request)) #debug to see the ip of the ip who requests a piece
        
        ip_address = get_ip(request)
        Baneado = Banned.objects.filter(documentidentifier__exact=object.identifier).filter(ip__exact = ip_address)
        if len(Baneado) == 1:
            template = loader.get_template('infomessage.html')
            context = {'message': 'You have been banned. You can not participate'}
            return HttpResponse(template.render(context, request))
        
        divx = int(object.divx)
        divy = int(object.divy)
        

        #location = newrandomfindfreepiece(object.identifier, request.COOKIES['user'])
        location = ultimaterandomfindfreepiece(object.identifier, request.COOKIES['user'], divx, divy)

        if location[0] == "null":
            template = loader.get_template('infomessage.html')
            context = {'message': 'There are not available pieces in this project'}
            return HttpResponse(template.render(context, request))

        x = str(location[0])
        y = str(location[1])
        alreadygiven = location[2]
        
        #pieces = Piece.objects.filter(documentidentifier__exact=object.identifier).filter(xposition__exact=x).filter(yposition__exact=y)
        #piece = pieces[0]
        if alreadygiven == False:
            piece = Piece()
            piece.documentidentifier = object.identifier
            piece.identifier = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(15)) #we add the identifier
            piece.xposition = int(x)
            piece.yposition = int(y)
            piece.state = 'given'
            piece.owner = request.COOKIES['user'] #we add the identifier
        
        check_limit_storage() #comprobar que hay espacio
        
        image = object.docfile
        im = Image.open(image)

        tamanox = object.image_width
        tamanoy = object.image_height
        
        #size = im.size
        porcionx = tamanox/float(divx) #no se si dara problemas con generar floats
        porciony = tamanoy/float(divy)
        
        x = int(x)-1
        y = int(y)-1
        
        left = int(x*porcionx)
        top = int(y*porciony)
        right = int((x+1)*porcionx)
        bottom = int((y+1)*porciony)

        cropped_image = im.crop( (left, top, right, bottom) )
        sizes = cropped_image.size
        
        if alreadygiven == False:
            piece.xpixelposition = left
            piece.ypixelposition = top
            piece.width = sizes[0]
            piece.height = sizes[1]
  
        
        nameofthefile= 'filename="Column'+str(x+1)+'of'+str(int(divx)) + '-Row'+str(y+1)+'of'+str(int(divy))+ '.jpg"'
        
        response = HttpResponse(content_type='image/jpg')
        cropped_image.save(response, "JPEG")
        response['Content-Disposition'] = 'attachment; '+nameofthefile
        
        
        tempfile_io =BytesIO()
        cropped_image.save(tempfile_io, "JPEG")
        image_file = InMemoryUploadedFile(tempfile_io, None, 'piecetemp.jpg','image/jpeg',sys.getsizeof(tempfile_io), None)
        
        if alreadygiven == False:
            piece.image = image_file
            piece.given_date = timezone.now()
            piece.ip = get_ip(request)
            piece.save()
        

        return response
    else:
        template = loader.get_template('infomessage.html')
        context = {'message': 'givemepiece didnt receive any POST'}
        return HttpResponse(template.render(context, request))

def sendpiece(request): #AQUI SE RECIBEN Y SE GUARDAN LAS PIEZAS
        
        if request.method == 'POST':
            identifier = request.POST.get('identifier')
            owner = request.COOKIES['user']
            ip_address = get_ip(request)
            Baneado = Banned.objects.filter(documentidentifier__exact=identifier).filter(ip__exact = ip_address)
            if len(Baneado) == 1:
            	template = loader.get_template('infomessage.html')
            	context = {'message': 'You have been banned'}
            	return HttpResponse(template.render(context, request))
            pieces = Piece.objects.filter(documentidentifier__exact=identifier).filter(owner__exact = owner)
            if len(pieces) == 1:
                sizes = (Image.open(request.FILES['docfile'])).size
                piece = pieces[0]
                if (piece.state == "given") or (piece.state == "submited") :
                    if sizes[0] == piece.width and sizes[1] == piece.height: 
                        piece.image = request.FILES['docfile']
                        format = Image.open(piece.image).format
                        if format != "JPEG":
                            if format != "PNG":
                                template = loader.get_template('infomessage.html')
                                context = {'message': 'Format not allowed! Please use JPG or PNG'}
                                return HttpResponse(template.render(context, request))
                        piece.state = 'submited'
                        ip_address = get_ip(request)
                        piece.ip = ip_address
                        piece.save()
                        template = loader.get_template('infomessage.html')
                        context = {'message': 'Thanks!'}
                        return HttpResponse(template.render(context, request))
                    else:
                        template = loader.get_template('infomessage.html')
                        context = {'message': 'This is not the piece I gave you...The size is different'}
                        return HttpResponse(template.render(context, request))
                else:
                   template = loader.get_template('infomessage.html')
                   context = {'message': 'This piece has been accepted already'}
                   return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('infomessage.html')
                context = {'message': 'You didnt request any piece in this project yet'}
                return HttpResponse(template.render(context, request))
        else:
            template = loader.get_template('infomessage.html')
            context = {'message': 'Sendpiece didnt receive any POST'}
            return HttpResponse(template.render(context, request))


def administrate(request):
        if request.method == 'POST':
            liberate_list = request.POST.getlist('liberate') #identificador del projecto que contiene la pieza
            accept_list = request.POST.getlist('accept')
            liberatefromaccepted_list = request.POST.getlist('liberatefromaccepted')
            reject_list = request.POST.getlist('reject')
            banipfromgiven_list = request.POST.getlist('banipfromgiven')
            banipfromsubmited_list = request.POST.getlist('banipfromsubmited')
            allowagain_list =  request.POST.getlist('allowagain')
            
            newacceptedpieces = False;
            newacceptedpiecedocumentidentifier = None;

            for piece_id in liberate_list:
                piece = Piece.objects.get(identifier__exact=piece_id)
                piece.delete()

            for piece_id in liberatefromaccepted_list:
                piece = Piece.objects.get(identifier__exact=piece_id)
                piece.delete()

            for piece_id in accept_list:
                updatepiece = Piece.objects.get(identifier__exact=piece_id)
                updatepiece.state = "accepted"
                updatepiece.save()
                newacceptedpieces = True
                newacceptedpiecedocumentidentifier = updatepiece.documentidentifier

            for piece_id in reject_list:
                piece = Piece.objects.get(identifier__exact=piece_id)
                piece.delete()

            for piece_id in banipfromsubmited_list:
                piece = Piece.objects.get(identifier__exact=piece_id)
                
                if len(Banned.objects.filter(ip__exact=piece.ip).filter(documentidentifier__exact=piece.documentidentifier)) > 0: # si ya esta baneado(el usuario ha seleccionado banear varias veces)solo liberamos
                    piece = Piece.objects.get(identifier__exact=piece_id)
                    piece.delete()
                else:
                    newbanned = Banned(ip=piece.ip, documentidentifier=piece.documentidentifier)
                    newbanned.identifier = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(15))
                    newbanned.save()
                    piece.delete()

            for piece_id in banipfromgiven_list:
                piece = Piece.objects.get(identifier__exact=piece_id)
                
                if len(Banned.objects.filter(ip__exact=piece.ip).filter(documentidentifier__exact=piece.documentidentifier)) > 0: # si ya esta baneado(el usuario ha seleccionado banear varias veces)solo liberamos
                    piece.delete()
                else:
                    newbanned = Banned(ip=piece.ip, documentidentifier=piece.documentidentifier)
                    newbanned.identifier = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(15))
                    newbanned.save()
                    piece.delete()

            for allowagain in allowagain_list:
                allowagain = Banned.objects.get(identifier__exact=allowagain)
                allowagain.delete()

            if newacceptedpieces: #Si se ha aceptado alguna pieza, significa que hay nuevas piezas para nuestro mosaico, por lo tanto lo actualizamos
                updatemosaic(newacceptedpiecedocumentidentifier)
            
            template = loader.get_template('infomessage.html')
            context = {'message': 'Changes saved!'}
            return HttpResponse(template.render(context, request))
    


def newrandomfindfreepiece(docidentifier, user): #la posicion primera la devuelve como 0,0 
	x = "null"
	y = "null"
	pieces = Piece.objects.filter(documentidentifier__exact=docidentifier)
	piece_already_given = pieces.filter(owner__exact=user)
	if len(piece_already_given) > 0:
	    x = piece_already_given[0].xposition
	    y = piece_already_given[0].yposition

	else:
	    pieces_free = pieces.filter(state__exact='null')
	    if len(pieces_free) > 0:
	        randomnumber = randint(0,len(pieces_free)-1)
	        x = pieces_free[randomnumber].xposition
	        y = pieces_free[randomnumber].yposition

	return (x,y)



def ultimaterandomfindfreepiece(docidentifier, user, divx, divy): #la posicion primera la devuelve como 0,0 
	x = "null"
	y = "null"
	alreadygiven = False
	pieces = Piece.objects.filter(documentidentifier__exact=docidentifier)#encuentra las piezas que existen, es decir, que se han dado previamente
	piece_already_given = pieces.filter(owner__exact=user)
	if len(piece_already_given) > 0:
	    x = piece_already_given[0].xposition
	    y = piece_already_given[0].yposition
	    alreadygiven = True
	else:

	    xavailable = list(range(1, divx+1)) #list from 1 to divx
	    yavailable = list(range(1, divy+1)) #list from 1 to divy
	    
	    for piece in pieces:
	        xavailable.remove(piece.xposition) #we remove the position that have been already given
	        yavailable.remove(piece.yposition) #we remove the position that have been already given

	    if len(xavailable) > 0:
	        randomnumberx = randint(0,len(xavailable)-1)
	        randomnumbery = randint(0,len(yavailable)-1)
	        x = xavailable[randomnumberx]
	        y = yavailable[randomnumbery]
	        
	    
	return (x,y,alreadygiven)



def updatemosaic(id):
	
	documents = Document.objects.filter(identifier__exact=id)
	document = documents[0]
	img = Image.open(document.docfile)
	

	pieces = Piece.objects.filter(documentidentifier__exact=id).filter(state__exact="accepted")
	for piece in pieces:
	    offset = (piece.xpixelposition, piece.ypixelposition)
	    pieceimage = Image.open(piece.image)
	    img.paste(pieceimage, offset)
	
	#img.save(document.mosaic.path) #esto no estoy nada seguro que al emigrarlo al servidor funcione
	
	tempfile_io =BytesIO()
	img.save(tempfile_io, "JPEG")
	image_file = InMemoryUploadedFile(tempfile_io, None, 'mosaictemp.jpg','image/jpeg',sys.getsizeof(tempfile_io), None)
	document.mosaic = image_file
	document.save()
	
	
	return "0"

def faq(request): #debug of conf.html
	template = loader.get_template('faq.html')
	context = {}
	return HttpResponse(template.render(context, request))


def pruebaconfig(request): #debug of conf.html
	documents = Document.objects.latest('id')
	template = loader.get_template('conf.html')
	context = {'documents': documents}
	return HttpResponse(template.render(context, request))
	#return HttpResponse('he entrado a pruebaconfig')

def pruebainfomessage(request): #debug of conf.html
	template = loader.get_template('infomessage.html')
	context = {'message': 'Your beautiful example message'}
	return HttpResponse(template.render(context, request))
