USE tarea2;

-- Limpieza previa
DELETE FROM foto;
DELETE FROM contactar_por;
DELETE FROM aviso_adopcion;
DELETE FROM comuna;
DELETE FROM region;

-- 1. Regiones
INSERT INTO region (id, nombre) VALUES
(1, 'Metropolitana'),
(2, 'Valparaíso');

-- 2. Comunas
INSERT INTO comuna (id, nombre, region_id) VALUES
(1, 'Providencia', 1),
(2, 'Ñuñoa', 1),
(3, 'Las Condes', 1),
(4, 'Vitacura', 1),
(5, 'Viña del Mar', 2);

-- 3. Avisos de adopción
INSERT INTO aviso_adopcion
(id, fecha_ingreso, comuna_id, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion)
VALUES
(1, NOW(), 1, 'Barrio Italia', 'Juan', 'juan@mail.com', '+56911111111', 'perro', 1, 2, 'a', NOW() + INTERVAL 10 DAY, 'Perrito cariñoso de 2 años, necesita hogar.'),
(2, NOW(), 2, 'Plaza Ñuñoa', 'Ana', 'ana@mail.com', '+56922222222', 'gato', 2, 6, 'm', NOW() + INTERVAL 15 DAY, 'Dos gatitos juguetones de 6 meses.'),
(3, NOW(), 3, 'El Golf', 'Luis', 'luis@mail.com', '+56933333333', 'perro', 1, 3, 'a', NOW() + INTERVAL 20 DAY, 'Perro de 3 años muy tranquilo.'),
(4, NOW(), 4, 'La Dehesa', 'María', 'maria@mail.com', '+56944444444', 'gato', 1, 1, 'a', NOW() + INTERVAL 5 DAY, 'Gatito de 1 año, muy sociable.'),
(7, NOW(), 5, 'Centro Viña', 'Pedro', 'pedro@mail.com', '+56955555555', 'perro', 3, 4, 'm', NOW() + INTERVAL 30 DAY, 'Tres cachorros de 4 meses, necesitan adopción.');
(8, NOW(), 3, 'Centro', 'Sara', 'sarita@mail.com', '+56955555555', 'perro', 3, 4, 'm', NOW() + INTERVAL 30 DAY, 'Tres cachorros de 4 meses, necesitan adopción.');

-- 4. Fotos de cada aviso

-- 4. Fotos de cada aviso
INSERT INTO foto (id, ruta_archivo, nombre_archivo, actividad_id) VALUES
(1, 'img/perro1.jpeg', 'perro1.jpeg', 1),
(2, 'img/perro2.jpeg', 'perro2.jpeg', 1),
(3, 'img/gato1.jpeg', 'gato1.jpeg', 2),
(4, 'img/gato2.jpeg', 'gato2.jpeg', 2),
(5, 'img/perro3.jpeg', 'perro3.jpeg', 3),
(6, 'img/gato3.jpeg', 'gato3.jpeg', 4),
(7, 'img/perro4.jpeg', 'perro4.jpeg', 5),
(8, 'img/perro5.jpeg', 'perro5.jpeg', 5);

-- 5. Medios de contacto
INSERT INTO contactar_por (id, nombre, identificador, actividad_id) VALUES
(1, 'whatsapp', '+56911111111', 1),
(2, 'telegram', '@juan_dogs', 1),
(3, 'instagram', '@ana_cats', 2),
(4, 'X', '@gatitosNunoa', 2),
(5, 'whatsapp', '+56933333333', 3),
(6, 'otra', 'correo:luis@mail.com', 3),
(7, 'instagram', '@maria.gatos', 4),
(8, 'whatsapp', '+56955555555', 5),
(9, 'tiktok', '@perritosVina', 5);
