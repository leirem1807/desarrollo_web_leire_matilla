-- ============================================
--  TAREA 3 - Creación de tabla 'comentario'
-- ============================================

-- Usa la base de datos de tu proyecto
USE tarea2;

-- Si ya existía, elimínala para evitar conflictos
DROP TABLE IF EXISTS comentario;

-- Crear la tabla
CREATE TABLE comentario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aviso_id INT NOT NULL,
    nombre VARCHAR(80) NOT NULL,
    texto TEXT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_comentario_aviso
        FOREIGN KEY (aviso_id)
        REFERENCES aviso_adopcion(id)
        ON DELETE CASCADE
);

-- ============================================
--  Datos de prueba (opcional)
-- ============================================

INSERT INTO comentario (aviso_id, nombre, texto)
VALUES 
(1, 'María López', '¡Qué lindos cachorros! Espero encuentren hogar pronto.'),
(1, 'Juan Pérez', '¿Siguen disponibles para adopción?'),
(2, 'Ana Torres', 'Me interesa adoptar un gato, ¿a quién contacto?');
