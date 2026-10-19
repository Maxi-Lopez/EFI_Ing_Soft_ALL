from django.test import TestCase, Client
from django.urls import reverse

from .models import Categoria, Marca, Producto


class CatalogoModelTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre='GPUs', slug='gpus', activa=True
        )
        self.marca = Marca.objects.create(
            nombre='NVIDIA', slug='nvidia', activa=True
        )
        self.producto = Producto.objects.create(
            nombre='RTX 4080',
            slug='rtx-4080',
            sku='RTX4080-001',
            precio_lista=1200000.00,
            stock_total=10,
            activo=True,
            destacado=True,
            marca=self.marca,
            categoria=self.categoria,
        )

    def test_categoria_creacion(self):
        self.assertEqual(self.categoria.nombre, 'GPUs')
        self.assertEqual(self.categoria.slug, 'gpus')
        self.assertTrue(self.categoria.activa)

    def test_marca_creacion(self):
        self.assertEqual(self.marca.nombre, 'NVIDIA')
        self.assertEqual(self.marca.slug, 'nvidia')

    def test_producto_creacion(self):
        self.assertEqual(self.producto.nombre, 'RTX 4080')
        self.assertEqual(self.producto.sku, 'RTX4080-001')
        self.assertTrue(self.producto.destacado)
        self.assertEqual(self.producto.marca, self.marca)
        self.assertEqual(self.producto.categoria, self.categoria)

    def test_producto_stock_disponible(self):
        self.assertEqual(self.producto.stock_disponible, 10)

    def test_producto_precio_final_oferta(self):
        self.producto.precio_oferta = 1000000.00
        self.producto.save()
        self.assertEqual(self.producto.precio_oferta, 1000000.00)

    def test_categoria_nivel_raiz(self):
        self.assertEqual(self.categoria.nivel, 0)

    def test_categoria_subnivel(self):
        sub = Categoria.objects.create(
            nombre='GeForce', slug='geforce',
            categoria_padre=self.categoria, activa=True
        )
        self.assertEqual(sub.nivel, 1)


class CatalogoViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(
            nombre='GPUs', slug='gpus', activa=True
        )
        self.marca = Marca.objects.create(
            nombre='NVIDIA', slug='nvidia', activa=True
        )
        Producto.objects.create(
            nombre='RTX 4080', slug='rtx-4080', sku='RTX4080-001',
            precio_lista=1200000.00, stock_total=10, activo=True,
            destacado=True, marca=self.marca, categoria=self.categoria,
        )

    def test_inicio_template(self):
        response = self.client.get(reverse('catalogo:inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'NexusGamer')

    def test_listar_productos_api(self):
        response = self.client.get('/api/v1/catalogo/productos/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('results', data)  # paginado
        self.assertGreaterEqual(data['count'], 1)

    def test_detalle_producto_api(self):
        response = self.client.get(
            '/api/v1/catalogo/productos/rtx-4080/'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['slug'], 'rtx-4080')
        self.assertEqual(data['marca']['nombre'], 'NVIDIA')
        self.assertEqual(data['categoria']['nombre'], 'GPUs')

    def test_listar_categorias_api(self):
        response = self.client.get('/api/v1/catalogo/categorias/')
        self.assertEqual(response.status_code, 200)

    def test_listar_marcas_api(self):
        response = self.client.get('/api/v1/catalogo/marcas/')
        self.assertEqual(response.status_code, 200)

    def test_accion_destacados(self):
        response = self.client.get('/api/v1/catalogo/productos/destacados/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(len(data), 1)

    def test_accion_ofertas(self):
        response = self.client.get('/api/v1/catalogo/productos/ofertas/')
        self.assertEqual(response.status_code, 200)

    def test_accion_buscar(self):
        response = self.client.get('/api/v1/catalogo/productos/buscar/?q=RTX')
        self.assertEqual(response.status_code, 200)

    def test_filtro_por_marca(self):
        response = self.client.get(
            '/api/v1/catalogo/productos/?marca__slug=nvidia'
        )
        self.assertEqual(response.status_code, 200)

    def test_filtro_por_categoria(self):
        response = self.client.get(
            '/api/v1/catalogo/productos/?categoria__slug=gpus'
        )
        self.assertEqual(response.status_code, 200)
