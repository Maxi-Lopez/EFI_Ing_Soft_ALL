from django.shortcuts import render


def inicio(request):
    """Vista principal de bienvenida (template)."""
    contexto = {
        'titulo': 'NexusGamer',
        'subtitulo': 'Tu portal al gaming next-gen',
    }
    return render(request, 'catalogo/inicio.html', contexto)
