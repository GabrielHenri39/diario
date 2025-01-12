from django.shortcuts import render,redirect 
from .models import Pessoa,Diario
from datetime import datetime,timedelta
from django.db.models import Count
# Create your views here.

def home(request):
    textos = Diario.objects.order_by('create_at')[:3]
    pessoas = Pessoa.objects.all()

    # nomes = [pessoa.nome for pessoa in pessoas]
    # qtds = []
    # for pessoa in pessoas:
    #     qtd = Diario.objects.filter(pessoas=pessoa).count()
    #     qtds.append(qtd)


    pessoas_com_contagem = Pessoa.objects.annotate(qtd_diarios=Count('diario'))
    nomes = [pessoa.nome for pessoa in pessoas_com_contagem]
    qtds = [pessoa.qtd_diarios for pessoa in pessoas_com_contagem]

    return render(request, 'home.html', {'textos': textos, 'nomes': nomes, 'qtds': qtds})


def escrever(request):
    if request.method == "GET":
        pessoas = Pessoa.objects.all()
        textos = Diario.objects.order_by('create_at')   
        return render(request, 'escrever.html', {'pessoas': pessoas, 'textos': textos})
    else:
        titulo = request.POST.get("titulo")
        tags = request.POST.getlist("tags")
        pessoas = request.POST.getlist("pessoas")
        texto = request.POST.get("texto")

        if len(titulo.strip()) == 0 or len(texto.strip()) == 0:
            return redirect('escrever')

        diario = Diario(
            titulo=titulo,
            texto=texto
        )
        diario.set_tags(tags)
        diario.save()
        
        pessoa_objs = Pessoa.objects.filter(id__in=pessoas)
        diario.pessoas.add(*pessoa_objs)
        diario.save()

        '''for i in pessoas:
            pessoa = Pessoa.objects.get(id=i)
            diario.pessoas.add(pessoa)'''

        #TODO: Mensagens e erro e sucesso
        
        return redirect('escrever')
    
    
def cadastrar_pessoa(request):
    if request.method == 'GET':
        return render(request, 'pessoa.html')
    else:
        nome = request.POST.get('nome')
        foto = request.FILES.get('foto')

        pessoa = Pessoa(
            nome=nome,
            foto=foto
        )
        pessoa.save()
        return redirect('escrever')
    
def dia(request):
    data = request.GET.get('data')
    data_formatada = datetime.strptime(data, '%Y-%m-%d')
    diarios = Diario.objects.filter(create_at__gte=data_formatada).filter(create_at__lte=data_formatada + timedelta(days=1))

    return render(request, 'dia.html', {'diarios': diarios, 'total': diarios.count(), 'data': data})

def excluir_dia(request):
    dia = datetime.strptime(request.GET.get('data'), '%Y-%m-%d')
    diarios = Diario.objects.filter(create_at__gte=dia).filter(create_at__lte=dia + timedelta(days=1))
    diarios.delete()
    return redirect('escrever')
