-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 12-05-2026 a las 15:59:10
-- Versión del servidor: 8.0.43
-- Versión de PHP: 7.4.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `makeupvela`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administradores`
--

CREATE TABLE `administradores` (
  `id` int NOT NULL,
  `nombre` text COLLATE utf8mb4_spanish_ci NOT NULL,
  `correo` text COLLATE utf8mb4_spanish_ci NOT NULL,
  `contraseña` varchar(15) COLLATE utf8mb4_spanish_ci NOT NULL,
  `fecha_creación` datetime NOT NULL,
  `nombre_img` varchar(35) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito_compras`
--

CREATE TABLE `carrito_compras` (
  `id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `fecha_creacion` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id` int NOT NULL,
  `nombre` varchar(30) COLLATE utf8mb4_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id`, `nombre`) VALUES
(1, 'Rostro'),
(2, 'Labios'),
(3, 'Ojos'),
(4, 'Acabado y preparaciÃ³n');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cesta`
--

CREATE TABLE `cesta` (
  `id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `fecha_creacion` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cesta_productos`
--

CREATE TABLE `cesta_productos` (
  `id` int NOT NULL,
  `cesta_id` int NOT NULL,
  `productos_id` int NOT NULL,
  `cantidad` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalles_carrito`
--

CREATE TABLE `detalles_carrito` (
  `id` int NOT NULL,
  `carrito_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `producto_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalles_pedido`
--

CREATE TABLE `detalles_pedido` (
  `id` int NOT NULL,
  `pedido_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `envios`
--

CREATE TABLE `envios` (
  `id` int NOT NULL,
  `pedido_id` int NOT NULL,
  `direccion_envio` text CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `fecha_envio` datetime NOT NULL,
  `estado_envios` text CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `fecha_pedido` datetime NOT NULL,
  `total` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int NOT NULL,
  `nombre` text COLLATE utf8mb4_spanish_ci NOT NULL,
  `descripción` text COLLATE utf8mb4_spanish_ci NOT NULL,
  `precio` float NOT NULL,
  `categoria_id` int NOT NULL,
  `fecha_creación` datetime NOT NULL,
  `nombre_img` varchar(30) COLLATE utf8mb4_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `nombre`, `descripción`, `precio`, `categoria_id`, `fecha_creación`, `nombre_img`) VALUES
(1, 'Base lÃ­quida', 'Alta cobertura', 18.75, 1, '2023-05-12 00:00:00', 'Base_lÃ­quida.jpg'),
(2, 'Labial mate', 'Larga duraciÃ³n', 12.5, 2, '2023-06-20 00:00:00', 'Labial_mate.png'),
(3, 'Delineador negro', 'Resistente al agua', 9.99, 3, '2023-07-15 00:00:00', 'Delineador_negro.jpg'),
(4, 'MÃ¡scara pestaÃ±as', 'Volumen extremo', 15.3, 4, '2023-08-01 00:00:00', 'MÃ¡scara_pestaÃ±as.png'),
(5, 'Polvo compacto', 'Acabado mate', 14.2, 1, '2023-09-10 00:00:00', 'Polvo_compacto.jpg'),
(6, 'Rubor rosa', 'Tonos naturales', 11.8, 2, '2023-04-22 00:00:00', 'Rubor_rosa.png'),
(7, 'Sombras nude', 'Tonos intensos', 20, 3, '2023-03-18 00:00:00', 'Sombras_nude.jpg'),
(8, 'Iluminador glow', 'Efecto brillante', 16.45, 4, '2023-02-14 00:00:00', 'Iluminador_glow.png'),
(9, 'Corrector lÃ­quido', 'Alta cobertura', 13.6, 1, '2023-01-30 00:00:00', 'Corrector_lÃ­quido.jpg'),
(10, 'Primer facial', 'Textura ligera', 17.25, 2, '2023-06-05 00:00:00', 'Primer_facial.png'),
(11, 'Base lÃ­quida', 'Hidratante', 19.1, 1, '2023-07-11 00:00:00', 'Base_lÃ­quida.jpg'),
(12, 'Labial mate', 'Acabado mate', 10.99, 2, '2023-08-09 00:00:00', 'Labial_mate.png'),
(13, 'Delineador negro', 'FÃ¡cil aplicaciÃ³n', 8.75, 3, '2023-09-02 00:00:00', 'Delineador_negro.jpg'),
(14, 'MÃ¡scara pestaÃ±as', 'Larga duraciÃ³n', 16, 4, '2023-05-25 00:00:00', 'MÃ¡scara_pestaÃ±as.png'),
(15, 'Polvo compacto', 'Textura ligera', 13.5, 1, '2023-04-18 00:00:00', 'Polvo_compacto.jpg'),
(16, 'Rubor rosa', 'Acabado natural', 12.2, 2, '2023-03-30 00:00:00', 'Rubor_rosa.png'),
(17, 'Sombras nude', 'Alta pigmentaciÃ³n', 21.3, 3, '2023-02-11 00:00:00', 'Sombras_nude.jpg'),
(18, 'Iluminador glow', 'Efecto glow', 15.9, 4, '2023-01-21 00:00:00', 'Iluminador_glow.png'),
(19, 'Corrector lÃ­quido', 'Cobertura media', 14, 1, '2023-06-17 00:00:00', 'Corrector_lÃ­quido.jpg'),
(20, 'Primer facial', 'Suaviza piel', 18.75, 2, '2023-07-29 00:00:00', 'Primer_facial.png'),
(21, 'Base lÃ­quida', 'Larga duraciÃ³n', 20.1, 1, '2023-08-15 00:00:00', 'Base_lÃ­quida.jpg'),
(22, 'Labial mate', 'Tonos intensos', 11.4, 2, '2023-09-01 00:00:00', 'Labial_mate.png'),
(23, 'Delineador negro', 'PrecisiÃ³n alta', 9.2, 3, '2023-05-03 00:00:00', 'Delineador_negro.jpg'),
(24, 'MÃ¡scara pestaÃ±as', 'Volumen alto', 17.1, 4, '2023-04-07 00:00:00', 'MÃ¡scara_pestaÃ±as.png'),
(25, 'Polvo compacto', 'Matificante', 13.9, 1, '2023-03-19 00:00:00', 'Polvo_compacto.jpg'),
(26, 'Rubor rosa', 'Color suave', 10.75, 2, '2023-02-25 00:00:00', 'Rubor_rosa.png'),
(27, 'Sombras nude', 'Paleta completa', 22, 3, '2023-01-10 00:00:00', 'Sombras_nude.jpg'),
(28, 'Iluminador glow', 'Brillo intenso', 16.8, 4, '2023-06-13 00:00:00', 'Iluminador_glow.png'),
(29, 'Corrector lÃ­quido', 'Cubre ojeras', 13.7, 1, '2023-07-04 00:00:00', 'Corrector_lÃ­quido.jpg'),
(30, 'Primer facial', 'Control grasa', 19.25, 2, '2023-08-20 00:00:00', 'Primer_facial.png'),
(31, 'Base lÃ­quida', 'Acabado natural', 18.95, 1, '2023-09-11 00:00:00', 'Base_lÃ­quida.jpg'),
(32, 'Labial mate', 'DuraciÃ³n larga', 12.1, 2, '2023-05-27 00:00:00', 'Labial_mate.png'),
(33, 'Delineador negro', 'Waterproof', 8.99, 3, '2023-04-14 00:00:00', 'Delineador_negro.jpg'),
(34, 'MÃ¡scara pestaÃ±as', 'PestaÃ±as largas', 16.7, 4, '2023-03-06 00:00:00', 'MÃ¡scara_pestaÃ±as.png'),
(35, 'Polvo compacto', 'Control brillo', 14.6, 1, '2023-02-17 00:00:00', 'Polvo_compacto.jpg'),
(36, 'Rubor rosa', 'Textura suave', 11.95, 2, '2023-01-28 00:00:00', 'Rubor_rosa.png'),
(37, 'Sombras nude', 'Tonos cÃ¡lidos', 20.8, 3, '2023-06-09 00:00:00', 'Sombras_nude.jpg'),
(38, 'Iluminador glow', 'Luminosidad alta', 15.6, 4, '2023-07-22 00:00:00', 'Iluminador_glow.png'),
(39, 'Corrector lÃ­quido', 'Alta duraciÃ³n', 13.3, 1, '2023-08-30 00:00:00', 'Corrector_lÃ­quido.jpg'),
(40, 'Primer facial', 'Base perfecta', 18.4, 2, '2023-09-05 00:00:00', 'Primer_facial.png'),
(41, 'Base lÃ­quida', 'Cobertura total', 21, 1, '2023-05-16 00:00:00', 'Base_lÃ­quida.jpg'),
(42, 'Labial mate', 'Color intenso', 11.75, 2, '2023-04-03 00:00:00', 'Labial_mate.png'),
(43, 'Delineador negro', 'Trazo fino', 9.1, 3, '2023-03-12 00:00:00', 'Delineador_negro.jpg'),
(44, 'MÃ¡scara pestaÃ±as', 'Efecto volumen', 17.5, 4, '2023-02-20 00:00:00', 'MÃ¡scara_pestaÃ±as.png'),
(45, 'Polvo compacto', 'Acabado suave', 14.1, 1, '2023-01-15 00:00:00', 'Polvo_compacto.jpg'),
(46, 'Rubor rosa', 'Tono natural', 12, 2, '2023-06-01 00:00:00', 'Rubor_rosa.png'),
(47, 'Sombras nude', 'Colores neutros', 21.5, 3, '2023-07-18 00:00:00', 'Sombras_nude.jpg'),
(48, 'Iluminador glow', 'Brillo suave', 16.2, 4, '2023-08-27 00:00:00', 'Iluminador_glow.png'),
(49, 'Corrector lÃ­quido', 'Oculta imperfecciones', 13.9, 1, '2023-09-09 00:00:00', 'Corrector_lÃ­quido.jpg'),
(50, 'Primer facial', 'Prebase ideal', 19, 2, '2023-05-08 00:00:00', 'Primer_facial.png');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` int NOT NULL,
  `nombre` varchar(50) COLLATE utf8mb4_spanish_ci NOT NULL,
  `correo` varchar(50) COLLATE utf8mb4_spanish_ci NOT NULL,
  `clave` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `perfil` char(1) COLLATE utf8mb4_spanish_ci NOT NULL DEFAULT 'U'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `nombre`, `correo`, `clave`, `perfil`) VALUES
(1, 'KARLA', 'karla.vela5112@alumnos.udg.mx', 'scrypt:32768:8:1$R0aXA3A3gub0U3G8$35d1a50eb1ecfcd930b668f8d545f242db59bbd344344f77bacc1186263bccca91b81d5f822129883c68044eea821cb4a3007ad8df28d0488663e273b1b2beb6', 'A'),
(2, 'GENARO', 'genaro@gmai.com', 'scrypt:32768:8:1$SN5fJj8iLE4grlk1$89c07b79da9efe3f8175d8f06f815e44e86bcac44346dfaa0d2fd4357415f896167f575d6c407f7a93a1a7af22af9a6b66e1c15c3ef139bd260c198dc5611bee', 'U');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios_finales`
--

CREATE TABLE `usuarios_finales` (
  `id` int NOT NULL,
  `nombre` varchar(30) COLLATE utf8mb4_spanish_ci NOT NULL,
  `correo` varchar(50) COLLATE utf8mb4_spanish_ci NOT NULL,
  `clave` varchar(200) COLLATE utf8mb4_spanish_ci NOT NULL,
  `fecha_creación` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administradores`
--
ALTER TABLE `administradores`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `carrito_compras`
--
ALTER TABLE `carrito_compras`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `detalles_carrito`
--
ALTER TABLE `detalles_carrito`
  ADD PRIMARY KEY (`id`),
  ADD KEY `carrito_id` (`carrito_id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indices de la tabla `detalles_pedido`
--
ALTER TABLE `detalles_pedido`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pedido_id` (`pedido_id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `categoria_id` (`categoria_id`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- Indices de la tabla `usuarios_finales`
--
ALTER TABLE `usuarios_finales`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `administradores`
--
ALTER TABLE `administradores`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `carrito_compras`
--
ALTER TABLE `carrito_compras`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `detalles_carrito`
--
ALTER TABLE `detalles_carrito`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detalles_pedido`
--
ALTER TABLE `detalles_pedido`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios_finales`
--
ALTER TABLE `usuarios_finales`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `carrito_compras`
--
ALTER TABLE `carrito_compras`
  ADD CONSTRAINT `carrito_compras_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `detalles_carrito`
--
ALTER TABLE `detalles_carrito`
  ADD CONSTRAINT `detalles_carrito_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `detalles_carrito_ibfk_2` FOREIGN KEY (`carrito_id`) REFERENCES `carrito_compras` (`id`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `detalles_pedido`
--
ALTER TABLE `detalles_pedido`
  ADD CONSTRAINT `detalles_pedido_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `detalles_pedido_ibfk_2` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categorias` (`id`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
