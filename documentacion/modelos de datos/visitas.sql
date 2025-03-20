-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 10-03-2025 a las 03:54:26
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `visitas`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `archivos`
--

CREATE TABLE `archivos` (
  `id_archivo` int(11) NOT NULL,
  `id_intercambio` int(11) DEFAULT NULL,
  `nombre_archivo` varchar(255) DEFAULT NULL,
  `tipo_archivo` varchar(50) DEFAULT NULL,
  `ruta_archivo` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `archivos`
--

INSERT INTO `archivos` (`id_archivo`, `id_intercambio`, `nombre_archivo`, `tipo_archivo`, `ruta_archivo`) VALUES
(75, 35, 'PM1 - 976.pdf', 'pdf', 'uploads\\pdfs\\PM1 - 976\\PM1 - 976.pdf');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `archivos_verificacion`
--

CREATE TABLE `archivos_verificacion` (
  `id_archivos_verificacion` int(11) NOT NULL,
  `verificacion_id` int(11) DEFAULT NULL,
  `nombre_archivo` varchar(255) DEFAULT NULL,
  `ruta_archivo` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `archivos_visita_tecnica`
--

CREATE TABLE `archivos_visita_tecnica` (
  `id_archivo_tecnica` int(11) NOT NULL,
  `visita_tecnica_id` int(11) NOT NULL,
  `nombre_archivo` varchar(255) NOT NULL,
  `ruta_archivo` varchar(255) NOT NULL,
  `fecha_subida` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `componente_alimentario_1`
--

CREATE TABLE `componente_alimentario_1` (
  `id_componente_alimentario` int(11) NOT NULL,
  `id_visita_tecnica` int(11) NOT NULL,
  `muestra` int(11) DEFAULT NULL,
  `componente` varchar(255) DEFAULT NULL,
  `nivel_1` decimal(10,2) NOT NULL,
  `nivel_2` decimal(10,2) NOT NULL,
  `nivel_3` decimal(10,2) NOT NULL,
  `nivel_4` decimal(10,2) NOT NULL,
  `nivel_5` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `componente_alimentario_promedio`
--

CREATE TABLE `componente_alimentario_promedio` (
  `id_promedio` int(11) NOT NULL,
  `id_visita_tecnica` int(11) NOT NULL,
  `nivel_escolar` varchar(50) NOT NULL,
  `peso_patron_bebida` decimal(10,2) NOT NULL,
  `peso_patron_proteico` decimal(10,2) NOT NULL,
  `peso_patron_cereal` decimal(10,2) NOT NULL,
  `peso_patron_fruta` decimal(10,2) NOT NULL,
  `peso_obtenido_bebida` decimal(10,2) NOT NULL,
  `peso_obtenido_proteico` decimal(10,2) NOT NULL,
  `peso_obtenido_cereal` decimal(10,2) NOT NULL,
  `peso_obtenido_fruta` decimal(10,2) NOT NULL,
  `concepto_bebida` enum('Cumple','No Cumple','No Aplica') NOT NULL,
  `concepto_proteico` enum('Cumple','No Cumple','No Aplica') NOT NULL,
  `concepto_cereal` enum('Cumple','No Cumple','No Aplica') NOT NULL,
  `concepto_fruta` enum('Cumple','No Cumple','No Aplica') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalles_menu`
--

CREATE TABLE `detalles_menu` (
  `id_detalle_menu` int(11) NOT NULL,
  `id_intercambio` int(11) NOT NULL,
  `componente` varchar(255) NOT NULL,
  `menu_oficial` text NOT NULL,
  `menu_intercambio` text NOT NULL,
  `id_tipo_racion` int(11) NOT NULL,
  `numero_menu_oficial` int(11) NOT NULL,
  `numero_menu_intercambio` int(11) NOT NULL,
  `fecha_ejecucion` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalles_menu`
--

INSERT INTO `detalles_menu` (`id_detalle_menu`, `id_intercambio`, `componente`, `menu_oficial`, `menu_intercambio`, `id_tipo_racion`, `numero_menu_oficial`, `numero_menu_intercambio`, `fecha_ejecucion`) VALUES
(81, 35, 'LACTEOS, ALIMENTO PROTEICO, DERIVADO CEREAL, FRUTA, ENSALADA VERDURAS', 'SORBETE DE MARACUYA, CARNE DE RES PICADA, ARROZ BLANCO CON FRIJOLES GUISADOS Y TAJADAS DE PLATANO FRITO, MANGO PICADO, N/A', 'SORBETE DE GUAYABA, CARNE DE RES SALTEADA CON ZANAHORIA Y ARVEJA, ARROZ BLANCO Y PAPA CRIOLLA DORADA, BANANO, ensalada roja', 3, 13, 7, '2025-03-26');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dotacion_menaje`
--

CREATE TABLE `dotacion_menaje` (
  `id` int(11) NOT NULL,
  `id_infraestructura` int(11) NOT NULL,
  `item` varchar(255) NOT NULL,
  `cantidad` text NOT NULL,
  `estado` set('Bueno','Regular','Malo') NOT NULL,
  `propiedad` set('IEO','Operador') NOT NULL,
  `foto_menaje` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `firmas`
--

CREATE TABLE `firmas` (
  `id_firma` int(11) NOT NULL,
  `id_intercambio` int(11) NOT NULL,
  `nombre_operador` varchar(255) NOT NULL,
  `tarjeta_profesional` varchar(255) NOT NULL,
  `cargo` varchar(255) NOT NULL,
  `tipo_firma` enum('manual','foto') NOT NULL,
  `firma_manual_base64` text DEFAULT NULL,
  `firma_foto_ruta` varchar(255) DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `firmas`
--

INSERT INTO `firmas` (`id_firma`, `id_intercambio`, `nombre_operador`, `tarjeta_profesional`, `cargo`, `tipo_firma`, `firma_manual_base64`, `firma_foto_ruta`, `fecha`) VALUES
(77, 35, 'X', 'X', 'X', 'foto', NULL, 'uploads/soporte/PM1 - 976/Firma-AnyEraser.png', '2025-03-10 02:15:49'),
(78, 35, 'X', 'X', 'X', 'foto', NULL, 'uploads/soporte/PM1 - 976/Firma-AnyEraser.png', '2025-03-10 02:15:49');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `firmas_bodega`
--

CREATE TABLE `firmas_bodega` (
  `id_firma_bodega` int(11) NOT NULL,
  `id_visita` int(11) NOT NULL,
  `nombre_recibe` varchar(255) NOT NULL,
  `cargo_recibe` varchar(255) NOT NULL,
  `nombre_realiza` varchar(255) NOT NULL,
  `cargo_realiza` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `firmas_infraestructura`
--

CREATE TABLE `firmas_infraestructura` (
  `id_firma` int(11) NOT NULL,
  `id_infraestructura` int(11) NOT NULL,
  `nombre_representante_ieo` varchar(255) NOT NULL,
  `nombre_profesional` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `firmas_nutricionistas`
--

CREATE TABLE `firmas_nutricionistas` (
  `id` int(11) NOT NULL,
  `correo` varchar(255) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `cargo` varchar(255) NOT NULL,
  `firma_path` varchar(255) NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `firmas_nutricionistas`
--

INSERT INTO `firmas_nutricionistas` (`id`, `correo`, `nombre`, `cargo`, `firma_path`, `fecha_creacion`) VALUES
(1, 'daniel.quintero@cali.edu.co', 'Juan Jimenez', 'PAE', 'static/firmas\\Firma-removebg-preview.png', '2025-01-19 16:52:21'),
(2, 'daniel.quintero@cali.edu.co', 'Juan Jimenez', 'PAE', 'static/firmas\\Firma-removebg-preview.png', '2025-01-19 17:37:26'),
(3, 'Gabriela.giraldo@cali.edu.co', 'Gabriela', 'Nutricionista', 'static/firmas\\WhatsApp_Image_2025-02-21_at_3.42.31_PM.jpeg', '2025-03-03 17:08:41'),
(4, 'ana.carolina@cali.edu.co', 'jd', 'ud', 'static/firmas\\frame-marco-dorado-25.pnge.png', '2025-03-03 17:52:04'),
(5, 'daniel.quintero@cali.edu.co', 'Daniel Quintero', 'PAE', 'static/firmas\\Firma-AnyEraser.png', '2025-03-05 03:36:40'),
(6, 'daniel.quintero@cali.edu.co', 'Juan Jimenez', 'PAE', 'static/firmas\\Firma-AnyEraser.png', '2025-03-05 03:36:40'),
(7, 'qdanif@gmail.com', 'Daniel Quintero', 'PAE', 'static/firmas\\Firma-AnyEraser.png', '2025-03-05 03:47:48'),
(8, 'qdanif@gmail.com', 'Juan Jimenez', 'PAE', 'static/firmas\\Firma-AnyEraser.png', '2025-03-05 03:47:48');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `firmas_tecnica`
--

CREATE TABLE `firmas_tecnica` (
  `id_firma` int(11) NOT NULL,
  `id_visita_tecnica` int(11) NOT NULL,
  `nombre_representante` varchar(100) NOT NULL,
  `cedula_representante` varchar(10) NOT NULL,
  `nombre_profesional` varchar(100) NOT NULL,
  `cedula_profesional` varchar(10) NOT NULL,
  `fecha_firma` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `firmas_verificacion`
--

CREATE TABLE `firmas_verificacion` (
  `id_firma_verificacion` int(11) NOT NULL,
  `id_verificacion` int(11) DEFAULT NULL,
  `nombre_representante` varchar(255) DEFAULT NULL,
  `cargo_representante` varchar(255) DEFAULT NULL,
  `nombre_funcionario` varchar(255) DEFAULT NULL,
  `nombre_operador` varchar(255) DEFAULT NULL,
  `cargo_operador` varchar(255) DEFAULT NULL,
  `cedula_operador` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fotos_bodega`
--

CREATE TABLE `fotos_bodega` (
  `id_foto` int(11) NOT NULL,
  `id_visita` int(11) NOT NULL,
  `id_pregunta` int(11) NOT NULL,
  `nombre_archivo` varchar(255) NOT NULL,
  `fecha_subida` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial_cambios`
--

CREATE TABLE `historial_cambios` (
  `id_historia_cambios` int(11) NOT NULL,
  `modalidad` varchar(50) NOT NULL,
  `id_racion` int(11) NOT NULL,
  `valor_anterior` text DEFAULT NULL,
  `valor_nuevo` text DEFAULT NULL,
  `actualizado_por` varchar(100) DEFAULT NULL,
  `fecha_actualizacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `componente` varchar(255) DEFAULT NULL,
  `numero_menu` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `historial_cambios`
--

INSERT INTO `historial_cambios` (`id_historia_cambios`, `modalidad`, `id_racion`, `valor_anterior`, `valor_nuevo`, `actualizado_por`, `fecha_actualizacion`, `componente`, `numero_menu`) VALUES
(8, 'industrializado', 68, 'N/A', 'NO APLICA', 'Daniel Quintero J.', '2025-03-05 15:31:16', 'AZUCARES Y DULCES', 17);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `industrializado`
--

CREATE TABLE `industrializado` (
  `id_industrializado` int(11) NOT NULL,
  `semana` int(11) DEFAULT NULL,
  `numero_menu` int(11) DEFAULT NULL,
  `id_tipo_racion` int(11) DEFAULT NULL,
  `componentes` text DEFAULT NULL,
  `ingredientes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `industrializado`
--

INSERT INTO `industrializado` (`id_industrializado`, `semana`, `numero_menu`, `id_tipo_racion`, `componentes`, `ingredientes`) VALUES
(1, 1, 1, 1, 'LACTEOS', 'BEBIDA LACTEA CON AVENA UHT\r\n'),
(2, 1, 1, 1, 'DERIVADO CEREAL', 'MUFFINS SABOR A QUESO\r\n'),
(3, 1, 1, 1, 'FRUTA', 'N/A\r\n'),
(4, 1, 1, 1, 'AZUCARES Y DULCES', 'MANI CON UVAS PASAS\r\n'),
(5, 1, 2, 1, 'LACTEOS', 'LECHE ENTERA UHT\r\n'),
(6, 1, 2, 1, 'DERIVADO CEREAL', 'GALLETAS CUCA\r\n'),
(7, 1, 2, 1, 'FRUTA', 'MANZANA\r\n'),
(8, 1, 2, 1, 'AZUCARES Y DULCES', 'N/A'),
(9, 1, 3, 1, 'LACTEOS', 'BEBIDA LACTEA CON AVENA UHT\r\n'),
(10, 1, 3, 1, 'DERIVADO CEREAL', 'TORTA VETEADA\r\n'),
(11, 1, 3, 1, 'FRUTA', 'BANANO\r\n'),
(12, 1, 3, 1, 'AZUCARES Y DULCES', 'N/A'),
(13, 1, 4, 1, 'LACTEOS', 'LECHE ENTERA UHT\r\n'),
(14, 1, 4, 1, 'DERIVADO CEREAL', 'PAN MOJICON\r\n'),
(15, 1, 4, 1, 'FRUTA', 'MANGO\r\n'),
(16, 1, 4, 1, 'AZUCARES Y DULCES', 'N/A\r\n'),
(17, 1, 5, 1, 'LACTEOS', 'BEBIDA LACTEA CON AVENA UHT\r\n'),
(18, 1, 5, 1, 'DERIVADO CEREAL', 'TORTA SABOR A VAINILLA\r\n'),
(19, 1, 5, 1, 'FRUTA', 'N/A\r\n'),
(20, 1, 5, 1, 'AZUCARES Y DULCES', 'MIX DE FRUTOS SECOS\r\n'),
(21, 2, 6, 1, 'LACTEOS', 'BEBIDA LACTEA CON AVENA UHT\r\n'),
(22, 2, 6, 1, 'DERIVADO CEREAL', 'PAN SEDA\r\n'),
(23, 2, 6, 1, 'FRUTA', 'N/A\r\n'),
(24, 2, 6, 1, 'AZUCARES Y DULCES', 'COCADA\r\n'),
(25, 2, 7, 1, 'LACTEOS', 'LECHE ENTERA UHT\r\n'),
(26, 2, 7, 1, 'DERIVADO CEREAL', 'GALLETAS CUCA\r\n'),
(27, 2, 7, 1, 'FRUTA', 'MANDARINA\r\n'),
(28, 2, 7, 1, 'AZUCARES Y DULCES', 'N/A\r\n'),
(29, 2, 8, 1, 'LACTEOS', 'LECHE SABOR CHOCOLATE UHT\r\n'),
(30, 2, 8, 1, 'DERIVADO CEREAL', 'PAN HOJALDRADO\r\n'),
(31, 2, 8, 1, 'FRUTA', 'PERA\r\n'),
(32, 2, 8, 1, 'AZUCARES Y DULCES', 'N/A\r\n'),
(33, 2, 9, 1, 'LACTEOS', 'LECHE ENTERA UHT\r\n'),
(34, 2, 9, 1, 'DERIVADO CEREAL', 'TORTA NEGRA\r\n'),
(35, 2, 9, 1, 'FRUTA', 'GUAYABA PERA\r\n'),
(36, 2, 9, 1, 'AZUCARES Y DULCES', 'N/A\r\n'),
(37, 2, 10, 1, 'LACTEOS', 'BEBIDA LACTEA CON AVENA UHT\r\n'),
(38, 2, 10, 1, 'DERIVADO CEREAL', 'TORTA SABOR A NARANJA\r\n'),
(39, 2, 10, 1, 'FRUTA', 'N/A\r\n'),
(40, 2, 10, 1, 'AZUCARES Y DULCES', 'MANI CONFITADO\r\n'),
(41, 3, 11, 1, 'LACTEOS', 'BEBIDA LACTEA CON AVENA UHT\r\n'),
(42, 3, 11, 1, 'DERIVADO CEREAL', 'MUFFINS CON CHIPS DE CHOCOLATE\r\n'),
(43, 3, 11, 1, 'FRUTA', 'PERA\r\n'),
(44, 3, 11, 1, 'AZUCARES Y DULCES', 'N/A\r\n'),
(45, 3, 12, 1, 'LACTEOS', 'LECHE ENTERA UHT\r\n'),
(46, 3, 12, 1, 'DERIVADO CEREAL', 'PAN COCO\r\n'),
(47, 3, 12, 1, 'FRUTA', 'N/A\r\n'),
(48, 3, 12, 1, 'AZUCARES Y DULCES', 'MANI CON UVAS PASAS\r\n'),
(49, 3, 13, 1, 'LACTEOS', 'LECHE SABOR CHOCOLATE UHT\r\n'),
(50, 3, 13, 1, 'DERIVADO CEREAL', 'PAN HOJALDRADO\r\n'),
(51, 3, 13, 1, 'FRUTA', 'MANDARINA\r\n'),
(52, 3, 13, 1, 'AZUCARES Y DULCES', 'N/A\r\n'),
(53, 3, 14, 1, 'LACTEOS', 'LECHE ENTERA UHT\r\n'),
(54, 3, 14, 1, 'DERIVADO CEREAL', 'MUFFINS SABOR A QUESO\r\n'),
(55, 3, 14, 1, 'FRUTA', 'BANANO\r\n'),
(56, 3, 14, 1, 'AZUCARES Y DULCES', 'N/A\r\n'),
(57, 3, 15, 1, 'LACTEOS', 'BEBIDA LACTEA CON AVENA UHT\r\n'),
(58, 3, 15, 1, 'DERIVADO CEREAL', 'GALLETAS CUCA\r\n'),
(59, 3, 15, 1, 'FRUTA', 'N/A\r\n'),
(60, 3, 15, 1, 'AZUCARES Y DULCES', 'BARRITA DE CEREAL\r\n'),
(61, 4, 16, 1, 'LACTEOS', 'LECHE ENTERA UHT\r\n'),
(62, 4, 16, 1, 'DERIVADO CEREAL', 'GALLETAS CUCA\r\n'),
(63, 4, 16, 1, 'FRUTA', 'N/A\r\n'),
(64, 4, 16, 1, 'AZUCARES Y DULCES', 'GELATINA BLANCA\r\n'),
(65, 4, 17, 1, 'LACTEOS', 'BEBIDA LACTEA CON AVENA UHT\r\n'),
(66, 4, 17, 1, 'DERIVADO CEREAL', 'PAN HOJALDRADO\r\n'),
(67, 4, 17, 1, 'FRUTA', 'MANGO\r\n'),
(68, 4, 17, 1, 'AZUCARES Y DULCES', 'NO APLICA'),
(69, 4, 18, 1, 'LACTEOS', 'LECHE ENTERA UHT\r\n'),
(70, 4, 18, 1, 'DERIVADO CEREAL', 'MUFFINS CON CHIPS DE CHOCOLATE\r\n'),
(71, 4, 18, 1, 'FRUTA', 'MANZANA\r\n'),
(72, 4, 18, 1, 'AZUCARES Y DULCES', 'N/A'),
(73, 4, 19, 1, 'LACTEOS', 'LECHE ENTERA UHT\r\n'),
(74, 4, 19, 1, 'DERIVADO CEREAL', 'TORTA DE CHOCOLATE\r\n'),
(75, 4, 19, 1, 'FRUTA', 'GRANADILLA\r\n'),
(76, 4, 19, 1, 'AZUCARES Y DULCES', 'N/A\r\n'),
(77, 4, 20, 1, 'LACTEOS', 'BEBIDA LACTEA CON AVENA UHT\r\n'),
(78, 4, 20, 1, 'DERIVADO CEREAL', 'PAN DE MAIZ\r\n'),
(79, 4, 20, 1, 'FRUTA', 'N/A\r\n'),
(80, 4, 20, 1, 'AZUCARES Y DULCES', 'MANI CONFITADO');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `infraestructura`
--

CREATE TABLE `infraestructura` (
  `id_infraestructura` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `municipio` varchar(100) NOT NULL,
  `corregimiento` varchar(100) NOT NULL,
  `vereda` varchar(100) NOT NULL,
  `operador` int(11) NOT NULL,
  `institucion` int(11) NOT NULL,
  `sede` int(11) NOT NULL,
  `codigo_sede` varchar(50) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `barrio` varchar(100) NOT NULL,
  `comuna` varchar(100) DEFAULT NULL,
  `zona` varchar(100) DEFAULT NULL,
  `tipo_racion` varchar(500) NOT NULL,
  `focalizacion` int(11) NOT NULL,
  `observacion_general` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `instituciones`
--

CREATE TABLE `instituciones` (
  `id_institucion` int(11) NOT NULL,
  `sede_educativa` varchar(255) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `id_operador` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `instituciones`
--

INSERT INTO `instituciones` (`id_institucion`, `sede_educativa`, `direccion`, `id_operador`) VALUES
(1, '01/01 JOSE HOLGUIN GARCES  - BARRIO TERRON COLORADO', 'AV. 4 OESTE NO 23-108 TERRON COLORADO', 1),
(2, '02/01 IE ISAIAS GAMBOA ', 'AV. 4 OESTE 12 - 05', 4),
(3, '03/01 IE LUIS FERNANDO CAICEDO - SEDE PRINCIPAL', 'AV 5A OESTE 47A - 04\r', 1),
(4, '04/01 IE TECNICO DE COMERCIO SANTA CECILIA 1', 'CALLE 61A NORTE  2GN - 62\r', 1),
(5, '05/01 IE DE SANTA LIBRADA', 'CALLE 7 NO. 14A - 106\r', 4),
(6, '06/01 IE NORMAL SUPERIOR FARALLONES DE CALI', 'CRA 22 NO. 2-65 OESTE\r', 1),
(7, '07/01 IE JORGE ISAACS - INEM', 'CRA 5 NORTE NO. 61 - 126\r', 1),
(8, '08/01 IE GUILLERMO VALENCIA', 'CRA 7 NORTE NO 45A08\r', 2),
(9, '09/01 IE REPUBLICA DE ISRAEL', 'CRA. 3 # 43-49\r', 4),
(10, '10/01 IE SANTO TOMAS  CASD', 'CALLE 34 # 3N-15\r', 1),
(11, '11/01 IE TECNICO INDUSTRIAL VEINTE DE JULIO', 'CARRERA 5 NORTE # 33-01\r', 1),
(12, '12/01 IE JOSE ANTONIO GALAN', 'CALLE 41 NO. 3N-11\r', 4),
(13, '13/01 IE LA MERCED', 'CALLE 47 # 4E-30\r', 2),
(14, '14/01 SIMON RODRIGUEZ - BARRIO SENA', 'CARRERA 1D BIS # 49-98\r', 2),
(15, '15/01 IE CELMIRA BUENO DE OREJUELA', 'CALLE 62B Nº 1A-9-250\r', 4),
(16, '16/01 IETI PEDRO ANTONIO MOLINA', 'CRA 1A 10 #71 00\r', 1),
(17, '17/01 IE MANUEL MARIA MALLARINO - BARRIO LAS CEIBAS', 'CRA 7 L  BIS NO. 63-00\r', 1),
(18, '18/01 JUAN BAUTISTA DE LA SALLE', 'CALLE 74 # 9-19\r', 4),
(19, '19/01 IE VICENTE BORRERO COSTA', 'CALLE 76N NO. 7S - 00\r', 2),
(20, '20/01 IE  SIETE DE AGOSTO', 'CALLE 72 # 11C - 27\r', 4),
(21, '21/01 IE JUAN DE AMPUDIA', 'CRA. 12 # 57-13\r', 2),
(22, '22/01 IE VILLACOLOMBIA', 'CR 12E N° 48 36\r', 2),
(23, '23/01 IE LAS AMERICAS - BARRIO AMERICAS', 'CARRERA 12 38-58\r', 2),
(24, '24/01 JOSE MANUEL SAAVEDRA GALINDO', 'CRA. 11 A NO. 28-25\r', 4),
(25, '25/01 ALBERTO CARVAJAL BORRERO', 'CRA 14  # 58 - 00\r', 2),
(26, '26/01 IE EVARISTO GARCIA ', 'CALLE 32 NO. 17 - 41\r', 2),
(27, '27/01 IE SANTA FE', 'CALLE  34  NO. 17B - 41\r', 2),
(28, '28/01 IE REPUBLICA DE ARGENTINA', 'CARRERA 11 D NO. 23-49\r', 2),
(29, '29/01 IE  ANTONIO JOSE CAMACHO', 'CRA 16 NO. 12-00\r', 3),
(30, '30/01 IE GENERAL ALFREDO VASQUEZ COBO - BARRIO ARANJUEZ', 'CALLE 15A NO. 22A - 37\r', 1),
(31, '31/01 IE NORMAL SUPERIOR SANTIAGO DE CALI', 'CRA 33A #12-60\r', 4),
(32, '32/01 JOSE MARIA CARBONELL - BARRIO PASOANCHO', 'CALLE 13 Nº 32 - 88\r', 4),
(33, '33/01 IE JOAQUIN DE CAYZEDO Y CUERO', 'CRA 35 # 15-33\r', 2),
(34, '34/01 IE RAFAEL NAVIA VARON', 'CLL 14 #48A-32\r', 4),
(35, '35/01 IE JOSE MARIA VIVAS BALCAZAR - BARRIO LA SELVA', 'CLL 14 #48A-32\r', 4),
(36, '36/01 IE CARLOS HOLGUIN LLOREDA', 'CRA. 40  NO. 18-85\r', 2),
(37, '37/01 IE AGUSTIN NIETO CABALLERO', 'KRA. 37 # 26C-51\r', 2),
(38, '38/01 IE BOYACA', 'CRA. 33A No. 25 - 25\r', 4),
(39, '39/01 IE DIEZ DE MAYO', 'CARRERA 25 A No. 26A-13\r', 3),
(40, '40/01 IE VILLA DEL SUR', 'CLL 30A N 41E - 99\r', 2),
(41, '41/01 IE CIUDAD MODELO', 'CARRERA 40 B No. 31C - 00\r', 3),
(42, '42/01 IE GENERAL FRANCISCO DE PAULA SANTANDER - BARRIO EL JARDIN', 'CALLE 27 31A-60 B/EL JARDIN\r', 3),
(43, '43/01 IE COMERCIAL CIUDAD DE CALI', 'CALLE 30 # 25-00\r', 4),
(44, '44/01 IE EVA RIASCOS PLATA', 'TRANVERSAL 25 DIAG. 26 - 69\r', 4),
(45, '45/01 IE TECNICA COMERCIAL HERNANDO NAVIA VARON', 'CRA 26P # 50-39\r', 1),
(46, '46/01 IE JUAN XXIII', 'CARRERA 28 C 50 - 16\r', 4),
(47, '47/01 IE JULIO CAICEDO Y TELLEZ', 'calle 59 N. 24E-40\r', 3),
(48, '48/01 IE INDUSTRIAL MARICE SINISTERRA', 'CALLE 39 # 25A - 43\r', 3),
(49, '49/01 IE BARTOLOME LOBOGUERRERO', 'CALLE 71 Nº 26E-25\r', 4),
(50, '50/01 IE HUMBERTO JORDAN MAZUERA', 'CRA 26 I #  D71A-25\r', 2),
(51, '51/01 IE JESUS VILLAFANE FRANCO', 'CALLE 72 P TRANSV. 72 S ESQUIN\r', 1),
(52, '52/01 IE SANTA ROSA SEDE  I', 'CALLE 72 X Nº 28-3 - 35\r', 1),
(53, '53/01 IE TECNICO INDUSTRIAL LUZ HAYDEE GUERRERO', 'CARRERA 28E2 No. 72S - 02\r', 2),
(54, '54/01 IE  EL DIAMANTE', 'CARRERA 31 No. 41-00\r', 2),
(55, '55/01 IE MONSENOR RAMON ARCILA', 'DIAGONAL 26 I3 TRANSV. 80A-18\r', 3),
(56, '56/01 IE LA ANUNCIACION', 'CRA 26 A No. 74-00\r', 3),
(57, '57/01 IE GABRIELA MISTRAL', 'CALLE 95 CRA. 27D ESQUINA\r', 3),
(58, '58/01 IEGABRIEL GARCIA MARQUEZ ', 'CRA 29B #54-00\r', 3),
(59, '59/01 IECARLOS HOLGUIN MALLARINO', 'CALLE 55A # 30B-50\r', 4),
(60, '60/01 IE CIUDAD CORDOBA', 'CALLE 50 # 49C-100\r', 4),
(61, '61/01 IE RODRIGO LLOREDA CAICEDO - BARRIO MARIANO RAMOS', 'CALLE 38A N. 47A-45 B/MARIANO RAMOS\r', 1),
(62, '62/01 IE CRISTOBAL COLON - BARRIO MARIANO RAMOS', 'CL. 44 Nº 47A-00 B/MARIANO RAMOS\r', 4),
(63, '63/01 IE DONALD RODRIGO TAFUR', 'CRA 43B #40-11\r', 3),
(64, '64/01 IE LIBARDO MADRID VALDERRAMA', 'CRA 41H No. 39-73\r', 3),
(65, '65/01 IE CARLOS HOLMES TRUJILLO', 'CALLE 44 CARRERA 43\r', 3),
(66, '66/01 IE TECNICO INDUSTRIAL COMUNA DIECISIETE', 'Cra 53 # 18 A-25\r', 2),
(67, '67/01 IE ALVARO ECHEVERRY', 'CLL 4  NO. 92-04\r', 3),
(68, '68/01 IE LA ESPERANZA', 'CRA 94 NO. 1A - 71 OESTE\r', 4),
(69, '69/01 IE JUAN PABLO II BARRIO PRADOS DEL SUR', 'CALLE 1A OESTE No. 78-23 B/PRADOS DEL SUR\r', 2),
(70, '70/01 IE LICEO DEPARTAMENTAL', 'CARRERA 37A 8-38\r', 3),
(71, '71/01 IE POLITECNICO MUNICIPAL DE CALI', 'CARRERA 62 2 - 28\r', 1),
(72, '72/01 IE EUSTAQUIO PALACIOS - BARRIO LIDO', 'CRA. 52 # 2-51\r', 1),
(73, '73/01 IE JUANA DE CAICEDO Y CUERO', 'CALLE 1 OESTE NO50-85\r', 1),
(74, '74/01 IE MULTIPROPOSITO', 'CRA. 56 NO. 7 OESTE - 190\r', 2),
(75, '75/01 IE TECNICA CIUDADELA DESEPAZ', 'CARRERA 23 NO 1206- 16\r', 2),
(76, '76/01 IE NAVARRO -  JUAN BAUTISTA DE LA SALLE', 'Corregimiento Navarro-\r', 4),
(77, '77/01 IE HORMIGUERO  -  PANTANO DE VARGAS', 'CRA. 143 CALLEJ CASCAJAL vereda cascajal\r', 4),
(78, '78/01 IE TECNICA DE BALLET CLASICO INCOLBALLET', 'KM 4 VIA JAMUNDI\r', 4),
(79, '79/01 IE PANCE ', 'Cgto Pance La Voragine KM1\r', 3),
(80, '80/01 IE LA BUITRERA JOSE MARIA GARCIA DE TOLEDO', 'CGTO LA BUITRERA KM 3cabecera\r', 3),
(81, '81/01 IE VILLACARMELO -CACIQUE CALARCA', 'VEREDA LA FONDA Cgto Villacarmelo\r', 3),
(82, '82/01 IE LOS ANDES -  TIERRA DE HOMBRES', 'CORREG. LOS ANDES  vda. Cabuyal\r', 3),
(83, '83/01  IE PICHINDE - JOSE HOLGUIN GARCES ', 'GOLONDRINAS CABECERA\r', 1),
(84, '84/01 IE FELIDIA - JOSE HOLGUIN GARCES ', 'CTO FELIDIA CABECERA\r', 1),
(85, '85/01 IE LA LEONERA ITA FARALLONES', 'CGTO LEONERA\r', 1),
(86, '86/01 IE SALADITO - FCO JOSE LLOREDA MERA ', 'CORREGIMIENTO EL SALADITO -\r', 2),
(87, '87/01 IE LA PAZ- SAAVEDRA GALINDO', 'CGTO LA PAZ, VEREDA VILLA DEL ROSARIO\r', 2),
(88, '88/01 IE MONTEBELLO', 'CGTO MONTEBELLO CABECERA\r', 1),
(89, '89/01 IE ALFONSO LOPEZ PUMAREJO', 'CARRERA 7S BIS CALLE 72 Y 73\r', 2),
(90, '90/01 IE GOLONDRINAS', 'GOLONDRINAS CABECERA\r', 2),
(91, '91/01 IE  NUEVO LATIR', 'Calle 76 No. 28- 20\r', 3),
(92, '92/01 IE  GENERAL JOSE MARIA CABAL ', 'Cl. 2c Oe. NO. 83-30\r', 3),
(93, 'ASODISVALLE - SEDE PRINCIPAL', 'Dg 71A1# 26I - 68\r', 1),
(94, 'TODAS LAS SEDES FOCALIZADAS', 'N/A', 1),
(95, 'TODAS LAS SEDES FOCALIZADAS', 'N/A', 2),
(96, 'TODAS LAS SEDES FOCALIZADAS', 'N/A', 3),
(97, 'TODAS LAS SEDES FOCALIZADAS', 'N/A', 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `instituciones_sedes`
--

CREATE TABLE `instituciones_sedes` (
  `id` int(11) NOT NULL,
  `id_institucion` int(11) DEFAULT NULL,
  `id_sede` int(11) DEFAULT NULL,
  `fecha_ejecucion` date DEFAULT NULL,
  `id_intercambio` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `instituciones_sedes`
--

INSERT INTO `instituciones_sedes` (`id`, `id_institucion`, `id_sede`, `fecha_ejecucion`, `id_intercambio`) VALUES
(225, 48, 179, '2025-03-26', 35),
(226, 48, 181, '2025-03-26', 35);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `intercambios`
--

CREATE TABLE `intercambios` (
  `id_intercambio` int(11) NOT NULL,
  `correo` varchar(255) NOT NULL,
  `fecha_solicitud` date NOT NULL DEFAULT curdate(),
  `id_operador` int(11) NOT NULL,
  `numero_intercambio` text NOT NULL,
  `id_tipo_racion` int(11) NOT NULL,
  `justificacion` varchar(255) NOT NULL,
  `justificacion_texto` text DEFAULT NULL,
  `concepto` varchar(20) DEFAULT 'Pendiente',
  `correo_operador` varchar(100) DEFAULT NULL,
  `asunto` varchar(1000) DEFAULT NULL,
  `mensaje` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `intercambios`
--

INSERT INTO `intercambios` (`id_intercambio`, `correo`, `fecha_solicitud`, `id_operador`, `numero_intercambio`, `id_tipo_racion`, `justificacion`, `justificacion_texto`, `concepto`, `correo_operador`, `asunto`, `mensaje`) VALUES
(35, 'componente.nutricional@cali.edu.co', '2025-03-09', 3, 'PM1 - 976', 3, 'Cancelacion Clases', 'NO', 'Pendiente', 'componente.nutricional@cali.edu.co', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `jornadaunica`
--

CREATE TABLE `jornadaunica` (
  `id_jornada_unica` int(11) NOT NULL,
  `semana` int(11) NOT NULL,
  `numero_menu` int(11) NOT NULL,
  `id_tipo_racion` int(11) NOT NULL,
  `componentes` text NOT NULL,
  `ingredientes` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `jornadaunica`
--

INSERT INTO `jornadaunica` (`id_jornada_unica`, `semana`, `numero_menu`, `id_tipo_racion`, `componentes`, `ingredientes`) VALUES
(1, 1, 1, 4, 'ALIMENTO PROTEICO', 'CARNE DE CERDO EN GOULASH CON HABICHUELA ZANAHORIA Y APIO\r\n'),
(2, 1, 1, 4, 'DERIVADO CEREAL', 'ARROZ CON PIMENTON\r\n'),
(3, 1, 1, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'PAPA CRIOLLA DORADA\r\n'),
(4, 1, 1, 4, 'VERDURA FRIA O CALIENTE', 'VERDURAS ENTRE LA PREPARACION PROTEICA\r\n'),
(5, 1, 1, 4, 'FRUTA', 'SORBETE DE GUAYABA\r\n'),
(6, 1, 1, 4, 'LACTEOS', 'INCLUIDO EN EL JUGO\r\n'),
(7, 1, 2, 4, 'ALIMENTO PROTEICO', 'FAJITAS DE PECHUGA DE POLLO ASADO LENTEJAS GUISADAS\r\n'),
(8, 1, 2, 4, 'DERIVADO CEREAL', 'ARROZ BLANCO'),
(9, 1, 2, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'YUCA DORADA\r\n'),
(10, 1, 2, 4, 'VERDURA FRIA O CALIENTE', 'ENSALADA DE LECHUGA ESPINACA TOMATE Y LIMON\r\n'),
(11, 1, 2, 4, 'FRUTA', 'JUGO DE LULO EN AGUA\r\n'),
(12, 1, 2, 4, 'LACTEOS', 'N/A'),
(13, 1, 3, 4, 'ALIMENTO PROTEICO', 'ESTOFADO DE CARNE DE CERDO CON PAPA\r\n'),
(14, 1, 3, 4, 'DERIVADO CEREAL', 'ARROZ CON FIDEO'),
(15, 1, 3, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'TAJADA DE PLATANO MADURO\r\n'),
(16, 1, 3, 4, 'VERDURA FRIA O CALIENTE', 'VERDURAS ORIENTALES (REPOLLO ZANAHORIA Y PIMENTON)\r\n'),
(17, 1, 3, 4, 'FRUTA', 'SORBETE DE GUANABANA\r\n'),
(18, 1, 3, 4, 'LACTEOS', 'INCLUIDO EN EL JUGO\r\n'),
(19, 1, 4, 4, 'ALIMENTO PROTEICO', 'HUEVOS PERICOS ARVEJAS GUISADAS\r\n'),
(20, 1, 4, 4, 'DERIVADO CEREAL', 'ARROZ BLANCO'),
(21, 1, 4, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'PLATANO MELADO\r\n'),
(22, 1, 4, 4, 'VERDURA FRIA O CALIENTE', 'ENSALADA DE REMOLACHA CON ZANAHORIA Y LIMON\r\n'),
(23, 1, 4, 4, 'FRUTA', 'JUGO DE PINA EN AGUA\r\n'),
(24, 1, 4, 4, 'LACTEOS', 'N/A\r\n'),
(25, 1, 5, 4, 'ALIMENTO PROTEICO', 'FAJITAS DE PECHUGA DE POLLO A LA JARDINERA\r\n'),
(26, 1, 5, 4, 'DERIVADO CEREAL', 'ARROZ CON PEREJIL\r\n'),
(27, 1, 5, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'PURE DE PAPA COMUN\r\n'),
(28, 1, 5, 4, 'VERDURA FRIA O CALIENTE', 'VERDURAS ENTRE LA PREPARACION PROTEICA\r\n'),
(29, 1, 5, 4, 'FRUTA', 'SORBETE DE MANGO\r\n'),
(30, 1, 5, 4, 'LACTEOS', 'INCLUIDO EN EL JUGO\r\n'),
(31, 2, 6, 4, 'ALIMENTO PROTEICO', 'CHOP SUEY DE POLLO (POLLO REPOLLO Y ZANAHORIA Y PIMENTON)\r\n'),
(32, 2, 6, 4, 'DERIVADO CEREAL', 'ARROZ BLANCO\r\n'),
(33, 2, 6, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'TAJADAS DE PLATANO MADURO\r\n'),
(34, 2, 6, 4, 'VERDURA FRIA O CALIENTE', 'VERDURAS ENTRE LA PREPARACION PROTEICA\r\n'),
(35, 2, 6, 4, 'FRUTA', 'SORBETE DE GUANABANA\r\n'),
(36, 2, 6, 4, 'LACTEOS', 'INCLUIDO EN EL JUGO\r\n'),
(37, 2, 7, 4, 'ALIMENTO PROTEICO', 'HUEVOS REVUELTOS LENTEJAS GUISADAS\r\n'),
(38, 2, 7, 4, 'DERIVADO CEREAL', 'ARROZ BLANCO\r\n'),
(39, 2, 7, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'PAPA GUISADA\r\n'),
(40, 2, 7, 4, 'VERDURA FRIA O CALIENTE', 'ENSALADA DE LECHUGA TOMATE Y PEPINO COHOMBRO\r\n'),
(41, 2, 7, 4, 'FRUTA', 'JUGO DE PINA EN AGUA\r\n'),
(42, 2, 7, 4, 'LACTEOS', 'N/A\r\n'),
(43, 2, 8, 4, 'ALIMENTO PROTEICO', 'CARNE DE CERDO CON AHUYAMA Y ARVEJA VERDE\r\n'),
(44, 2, 8, 4, 'DERIVADO CEREAL', 'ARROZ CON FIDEOS\r\n'),
(45, 2, 8, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'YUCA DORADA\r\n'),
(46, 2, 8, 4, 'VERDURA FRIA O CALIENTE', 'VERDURAS ENTRE LA PREPARACION PROTEICA\r\n'),
(47, 2, 8, 4, 'FRUTA', 'SORBETE DE FRESA\r\n'),
(48, 2, 8, 4, 'LACTEOS', 'INCLUIDO EN EL JUGO\r\n'),
(49, 2, 9, 4, 'ALIMENTO PROTEICO', 'FAJITAS DE CARNE DE RES ASADA FRIJOLES GUISADOS CON ZAPALLO\r\n'),
(50, 2, 9, 4, 'DERIVADO CEREAL', 'ARROZ BLANCO\r\n'),
(51, 2, 9, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'MONEDITAS DE PLATANO\r\n'),
(52, 2, 9, 4, 'VERDURA FRIA O CALIENTE', 'ENSALADA DE: LECHUGA TOMATE Y AGUACATE\r\n'),
(53, 2, 9, 4, 'FRUTA', 'JUGO DE GUAYABA EN AGUA\r\n'),
(54, 2, 9, 4, 'LACTEOS', 'N/A\r\n'),
(55, 2, 10, 4, 'ALIMENTO PROTEICO', 'CHULETA DE CERDO\r\n'),
(56, 2, 10, 4, 'DERIVADO CEREAL', 'ARROZ CON PEREJIL\r\n'),
(57, 2, 10, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'INCLUIDO EN LA ENSALADA\r\n'),
(58, 2, 10, 4, 'VERDURA FRIA O CALIENTE', 'ENSALADA DE PAPA (PAPA EN CUADRITOS) ZANAHORIA EN CUBOS ARVEJA Y HABICHUELA CON SALSA BLANCA\r\n'),
(59, 2, 10, 4, 'FRUTA', 'SORBETE DE MANGO\r\n'),
(60, 2, 10, 4, 'LACTEOS', 'INCLUIDO EN EL JUGO\r\n'),
(61, 3, 11, 4, 'ALIMENTO PROTEICO', 'TROZOS DE CARNE DE CERDO CON ZANAHORIA Y HABICHUELA\r\n'),
(62, 3, 11, 4, 'DERIVADO CEREAL', 'ARROZ CON CILANTRO\r\n'),
(63, 3, 11, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'TROZO DE PLATANO MADURO COCIDO\r\n'),
(64, 3, 11, 4, 'VERDURA FRIA O CALIENTE', 'VERDURAS ENTRE LA PREPARACION PROTEICA\r\n'),
(65, 3, 11, 4, 'FRUTA', 'SORBETE DE MANGO\r\n'),
(66, 3, 11, 4, 'LACTEOS', 'INCLUIDO EN EL JUGO\r\n'),
(67, 3, 12, 4, 'ALIMENTO PROTEICO', 'FAJITAS DE POLLO EN SALSA CRIOLLA BLANQUILLOS GUISADOS\r\n'),
(68, 3, 12, 4, 'DERIVADO CEREAL', 'ARROZ BLANCO\r\n'),
(69, 3, 12, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'PAPA CRIOLLA DORADA\r\n'),
(70, 3, 12, 4, 'VERDURA FRIA O CALIENTE', 'ENSALADA DE TOMATE Y LECHUGA CON LIMON\r\n'),
(71, 3, 12, 4, 'FRUTA', 'JUGO DE GUAYABA EN AGUA\r\n'),
(72, 3, 12, 4, 'LACTEOS', 'N/A\r\n'),
(73, 3, 13, 4, 'ALIMENTO PROTEICO', 'TROZOS DE CARNE DE CERDO SALTEADOS\r\n'),
(74, 3, 13, 4, 'DERIVADO CEREAL', 'ARROZ BLANCO\r\n'),
(75, 3, 13, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'PAPA EN SALSA DE MARGARINA CILANTRO Y LECHE\r\n'),
(76, 3, 13, 4, 'VERDURA FRIA O CALIENTE', 'VERDURAS SALTEADAS (BROCOLI HABICHUELA ZANAHORIA Y CEBOLLA)\r\n'),
(77, 3, 13, 4, 'FRUTA', 'SORBETE DE TOMATE DE ARBOL\r\n'),
(78, 3, 13, 4, 'LACTEOS', 'INCLUIDO EN EL JUGO\r\n'),
(79, 3, 14, 4, 'ALIMENTO PROTEICO', 'HUEVOS REVUELTOS ARVEJA GUISADA CON PAPA\r\n'),
(80, 3, 14, 4, 'DERIVADO CEREAL', 'ARROZ BLANCO\r\n'),
(81, 3, 14, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'YUCA DORADA\r\n'),
(82, 3, 14, 4, 'VERDURA FRIA O CALIENTE', 'ENSALADA DULCE: REPOLLO ZANAHORIA Y PINA CALADA\r\n'),
(83, 3, 14, 4, 'FRUTA', 'JUGO DE MARACUYA EN AGUA\r\n'),
(84, 3, 14, 4, 'LACTEOS', 'N/A\r\n'),
(85, 3, 15, 4, 'ALIMENTO PROTEICO', 'FAJITAS DE POLLO CON ESPINACA CEBOLLA Y PIMENTON\r\n'),
(86, 3, 15, 4, 'DERIVADO CEREAL', 'ARROZ BLANCO\r\n'),
(87, 3, 15, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'PURA DE PAPA AMARILLA\r\n'),
(88, 3, 15, 4, 'VERDURA FRIA O CALIENTE', 'VERDURAS ENTRE LA PREPARACION PROTEICA\r\n'),
(89, 3, 15, 4, 'FRUTA', 'SORBETE DE GUAYABA\r\n'),
(90, 3, 15, 4, 'LACTEOS', 'INCLUIDO EN EL JUGO\r\n'),
(91, 4, 16, 4, 'ALIMENTO PROTEICO', 'FAJITAS DE CARNE DE CERDO ASADA\r\n'),
(92, 4, 16, 4, 'DERIVADO CEREAL', 'ARROZ CON PEREJIL\r\n'),
(93, 4, 16, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'YUCA GUISADA\r\n'),
(94, 4, 16, 4, 'VERDURA FRIA O CALIENTE', 'ENSALADA DE REMOLACHA CON ZANAHORIA Y LIMON\r\n'),
(95, 4, 16, 4, 'FRUTA', 'SORBETE DE MANGO\r\n'),
(96, 4, 16, 4, 'LACTEOS', 'INCLUIDO EN EL JUGO\r\n'),
(97, 4, 17, 4, 'ALIMENTO PROTEICO', 'HUEVOS REVUELTOS LENTEJAS GUISADAS\r\n'),
(98, 4, 17, 4, 'DERIVADO CEREAL', 'ARROZ BLANCO\r\n'),
(99, 4, 17, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'PAPA CRIOLLA DORADA\r\n'),
(100, 4, 17, 4, 'VERDURA FRIA O CALIENTE', 'ENSALADA DE LECHUGA TOMATE Y PEPOINO\r\n'),
(101, 4, 17, 4, 'FRUTA', 'JUGO DE FRESA EN AGUA\r\n'),
(102, 4, 17, 4, 'LACTEOS', 'N/A'),
(103, 4, 18, 4, 'ALIMENTO PROTEICO', 'ESTOFADO DE CARNE DE RES CON HABICHUELA Y ZANAHORIA\r\n'),
(104, 4, 18, 4, 'DERIVADO CEREAL', 'ARROZ CON CILANTRO\r\n'),
(105, 4, 18, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'PLATANO MADURO\r\n'),
(106, 4, 18, 4, 'VERDURA FRIA O CALIENTE', 'ENSALADA DE LECHUGA TOMATE Y AGUACATE\r\n'),
(107, 4, 18, 4, 'FRUTA', 'SORBETE DE GUANABANA\r\n'),
(108, 4, 18, 4, 'LACTEOS', 'INCLUIDO EN EL JUGO'),
(109, 4, 19, 4, 'ALIMENTO PROTEICO', 'CARNE DE CERDO SALTEADO EN TROZOS FRIJOLES GUISADOS CON PLATANO\r\n'),
(110, 4, 19, 4, 'DERIVADO CEREAL', 'ARROZ BLANCO\r\n'),
(111, 4, 19, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'YUCAS COCIDAS\r\n'),
(112, 4, 19, 4, 'VERDURA FRIA O CALIENTE', 'ENSALADA DE REPOLLO Y ZANAHORIA\r\n'),
(113, 4, 19, 4, 'FRUTA', 'JUGO DE MARACUYA EN AGUA\r\n'),
(114, 4, 19, 4, 'LACTEOS', 'N/A\r\n'),
(115, 4, 20, 4, 'ALIMENTO PROTEICO', 'PECHUGA DE POLLO DESMECHADA EN SALSA BLANCA\r\n'),
(116, 4, 20, 4, 'DERIVADO CEREAL', 'ESPAGUETIS SALTEADOS Y ARROZ BLANCO\r\n'),
(117, 4, 20, 4, 'TUBERCULOS RAICES PLATANOS DERIVADOS CEREAL', 'N/A\r\n'),
(118, 4, 20, 4, 'VERDURA FRIA O CALIENTE', 'ENSALADA DE LECHUGA ZANAHORIA Y MANGO\r\n'),
(119, 4, 20, 4, 'FRUTA', 'SORBETE DE FRESA\r\n'),
(120, 4, 20, 4, 'LACTEOS', 'INCLUIDO EN EL JUGO\r\n');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `operadores`
--

CREATE TABLE `operadores` (
  `id_operador` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `numero_contrato` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `operadores`
--

INSERT INTO `operadores` (`id_operador`, `nombre`, `numero_contrato`) VALUES
(1, 'UNION TEMPORAL CONSTRUYENDO JUNTOS 2024', 974),
(2, 'FUNDACION PRO DESARROLLO COMUNITARIO POR COLOMBIA', 975),
(3, 'CORPORACION HACIA UN VALLE SOLIDARIO', 976),
(4, 'UNION TEMPORAL NUTRIENDO CALI 2024', 977);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `preguntas_bodega`
--

CREATE TABLE `preguntas_bodega` (
  `id_pregunta` int(11) NOT NULL,
  `numero` varchar(50) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `categoria` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `preguntas_bodega`
--

INSERT INTO `preguntas_bodega` (`id_pregunta`, `numero`, `descripcion`, `categoria`) VALUES
(1, '1.1', 'La planta está ubicada en un lugar aislado de cualquier foco de insalubridad que represente riesgo de contaminación.', 'Edificaciones e Instalaciones'),
(2, ' 1.2', 'El funcionamiento de la planta no pone en riesgo la salud y el bienestar de la comunidad.', 'Edificaciones e Instalaciones'),
(3, ' 1.3', 'Los accesos y alrededores están limpios y libres de acumulación de basuras. ', 'Edificaciones e Instalaciones'),
(4, ' 1.3a', 'Sus accesos y alrededores tienen superficies pavimentadas o recubiertas por superficies que faciliten el mantenimiento sanitario.', 'Edificaciones e Instalaciones'),
(5, ' 2.1', ' La edificación está diseñada y construida de manera que proteja los ambientes de producción e impida la entrada de polvo, lluvia, suciedades y otros componentes, así como el ingreso y refugio de plagas y animales domésticos.', 'Diseño y Construccion'),
(6, ' 2.2', 'La edificación posee una adecuada separación física y funcional de áreas de operación.', 'Diseño y Construccion'),
(7, '2.3', ' Los ambientes de la edificación, tienen el ambiente adecuado para la instalación, operación y mantenimiento de equipos.                                                         ', 'Diseño y Construccion'),
(8, '2.3.a', 'La edificación y sus diversos locales tienen el tamaño adecuado para la circulación del personal y traslado de la materia prima.                                                          ', 'Diseño y Construccion'),
(9, '2.4', 'La edificación y sus instalaciones están construidas para facilitar las operaciones de limpieza, desinfección y desinfestación.', 'Diseño y Construccion'),
(10, '2.5', 'El tamaño del almacén o depósito es proporcional a los volumenes de insumos y productos terminados manejados por el establecimiento disponiendo además de espacios libres para la circulación del personal, el traslado de materiales o productos y para realizar la limpieza y el mantenimiento de las áreas respectivas.', 'Diseño y Construccion'),
(11, '2.6', 'Sus áreas deberán estar separadas de cualquier tipo de vivienda y no podrán ser utilizadas como dormitorio.', 'Diseño y Construccion'),
(12, '2.7', 'No se permite la presencia de animales en los establecimientos objeto del presente decreto.', 'Diseño y Construccion'),
(13, '3.1/ 3.2/3.3/3.4/3.5', ' El agua es potable y cumple normas vigentes establecidas. Se dispone de agua potable a la temperatura y presión requeridas para efectuar una limpieza y desinfección efectiva.', 'Abastacimiento de Agua'),
(14, ' 4.1', ' Dispone de sistemas sanitarios adecuados para la recolección, tratamiento y disposición de aguas residuales.', 'Dispocision de Residuos Liquidos'),
(15, ' 4.2', 'El manejo de los residuos líquidos dentro del establecimiento se realiza de manera que impide la contaminación del alimento o de las superficies de potencial contacto con éste.', 'Dispocision de Residuos Liquidos'),
(16, '5.1, 5,2, 5.3, 5.4, 5.5', ' El establecimiento debe estar dotado de  un sistema de recoleccion y almacenamiento de residuos solidos que impida el acceso y ploriferacion de insectos, roedores, y otras plagas, el cual debe cumplir con las normas sanitarias vigentes', 'Dispocision de Residuos Solidos'),
(17, ' 6.1/6.2', 'Posee instalaciones sanitarias suficientes como servicios sanitarios para facilitar la higiene del personal (en buen estado) y se proveen de los recursos requeridos para la higiene tales como papel higiénico, dispensador de jabón, implementos desechables o equipos automaticos para el secado de manos y papeleras con bolsa de color determinado.', 'Instalaciones Sanitarias'),
(18, '6.3', 'Se encuentran instalados lavamanos en las áreas de elaboración o próximos a éstas para la higiene del personal que participa en la manipulación de alimentos para facilitar la supervisión de éstas prácticas.', 'Instalaciones Sanitarias'),
(19, ' 6.4', 'En las proximidades de los lavamanos se colocan avisos  o advertencias al personal sobre la necesidad de lavarse las manos luego de usar los servicios sanitarios, después de cualquier cambio de actividad y antes de iniciar labores de producción.', 'Instalaciones Sanitarias'),
(20, '6.5', 'Cuando lo requieran, deben disponerse en las áreas de elaboración de instalaciones adecuadas para la limpieza y desinfección  de los equipos y utensilios de trabajo.', 'Instalaciones Sanitarias'),
(21, 'ARTICULO 7  /11.1-1.4/2,2.1,2.2', '1. Pisos y Paredes: Sin grietas, rugosidades, asperezas o  falta de continuidad que facilite la acumulación de suciedad y/o afecte su limpieza, las uniones entre paredes, entre estas y con el piso son redondeadas. Las superficies son de color claro, impermeables, lavables y no absorbentes, esto es, que no permita el paso de ningún tipo de Líquido y de fácil eliminación de residuos. Los pisos cuentan con la pendiente necesaria para efectos de drenaje.\nDrenajes: Cuenta con las tuberías y drenajes, debidamente protegidos por rejillas para la conducción y recolección de aguas residuales; en caso de que se cuente con drenajes al interior de cavas o cuartos fríos, estos deben contar con mecanismo de sellado, que puedan ser removidos para facilitar las labores de limpieza y desinfección.', 'Areas de Especificaciones'),
(22, ' 3-4-5', 'Techos: Sin cortes ni grietas que acumulen polvo o suciedad y favorezcan el crecimiento de hongos que puedan caer sobre los alimentos o las superficies de trabajo, o que favorezcan el ingreso de plagas al establecimiento. En caso de contar con falsos techos, estos de deben ser construidos en material impermeable, resistente, liso, con acceso a la cámara superior para labores de limpieza, desinfección y desinsectación.\nVentilación: Ventanas y aberturas sin deterioro tales como grietas que produzcan acumulación de suciedad. Aquellas que lo requieran deberán contar con una malla que evite el ingreso plagas y que sea de fácil limpieza. El flujo de aire debe ser unidireccional (de una zona limpia a una sucia). Esta debe ser capaz de prevenir la condensación del vapor, acúmulo de polvo y facilitar la remoción del calor. Las estructuras elevadas como sistemas de extracción y/o extractores de aire, deben encontrarse en buen estado de mantenimiento que evite la caída de materias extrañas, además de ser de fácil limpieza y eliminación de la condensación que produzca goteo sobre los alimentos.\nPuertas: Ser resistentes, de superficie lisa y no absorbente, su diseño debe impedir el ingreso de plagas al establecimiento.\nIluminación: La iluminación puede ser natural o artificial, las lámparas deben encontrarse en buen estado de mantenimiento, ser de fácil limpieza y estar protegidas para evitar la caída de partículas extrañas sobre las superficies que entran en contacto con el alimento, sobre el alimento y sobre los manipuladores. ', 'Areas de Especificaciones'),
(23, 'ARTICULO 8/1', 'Los equipos y utensilios empleados en el manejo de los alimentos son de materiales resistentes al uso y a la corrosión y son de fácil  limpieza y desinfección.  ', 'CAPITULO II EQUIPOS Y UTENSILIOS'),
(24, '7', 'Las superficies de contacto con el alimento, no están recubiertas con pinturas u otro tipo de material desprendible.', 'CAPITULO II EQUIPOS Y UTENSILIOS'),
(25, '9', 'La superficie exterior de equipos está diseñada y construida para facilitar limpieza y desinfección.', 'CAPITULO II EQUIPOS Y UTENSILIOS'),
(26, '10', 'Las mesas y mesones empleados en el manejo de alimentos tienen superficies lisas, con bordes sin aristas y están construidas con materiales resistentes, impermeables y lavables.', 'CAPITULO II EQUIPOS Y UTENSILIOS'),
(27, '11', 'Los contenedores y recipientes usados para el almacenamiento de materiales no comestibles y desechos, son a prueba de fugas, debidamente identificados, en material impermeable, de fácil limpieza y con tapa hermética. Los mismos no son utilizados para contener productos comestibles.', 'CAPITULO II EQUIPOS Y UTENSILIOS'),
(28, 'ARTICULO 10/2', 'La distancia entre equipos y paredes perimetrales, columnas u otros, permite funcionar adecuadamente y facilita el acceso para limpieza, inspección y mantenimiento.', 'CAPITULO II EQUIPOS Y UTENSILIOS'),
(29, 'ARTICULO 11 /1-2', 'El personal manipulador de alimentos tiene reconocimiento médico antes de desempeñar esta función (incluye el conductor del vehiculo y ayudante), Efectuan un reconocimiento médico cada vez que se considere necesario por razones clínicas y epidemiológicas. ', 'CAPITULO III  MANIPULADOR DE ALIMENTOS'),
(30, '4', 'La dirección de la bodega toma las medidas correspondientes para que al personal manipulador de alimentos se le practique un reconocimiento médico, por lo menos una vez al año.', 'CAPITULO III  MANIPULADOR DE ALIMENTOS'),
(31, '5', 'La dirección de la bodega toma las medidas necesarias para que no se permita contaminar los alimentos directa o indirectamente a ninguna persona que se sepa o sospeche que padezca de una enfermedad susceptible de transmitirse por los alimentos. Todo manipulador de alimentos que represente un riesgo de este tipo lo comunica a la dirección de la bodega.', 'CAPITULO III  MANIPULADOR DE ALIMENTOS'),
(32, 'ARTICULO 12', 'Todas las personas que realizan actividades de manipulación de alimentos tienen formación en materia de educación sanitaria (BPM) y debe estar capacittado en las tareas que se le asignan. La empresa debe tener un plan de capacitacion continuo y permamente para el personal manipulador de alimentos desde el momento de su contrtacion y luego ser refrozado mediane charlas cursos u otros medios efectivos de actualizacion minimo 10 horas anuales.  ', 'EDUCACION Y CAPACITACION'),
(33, 'Parrafo 1', 'Para refrozar el cumplimiento de las practicas higienicas Se  colocan en sitios estratégicos avisos alusivos a la obligatoriedad y necesidad de su observancia durante la manipulación de alimentos.', 'EDUCACION Y CAPACITACION'),
(34, 'Parrafo 2', 'El manipulador de alimentos está entrenado para comprender y manejar el control de los puntos críticos que están bajo su responsabilidad y la importancia de su monitoreo. Ademas debe conocer los limites de punto del proceso y las acciones correctivas a tomar cuando existan desviaciones en dichos limites.', 'EDUCACION Y CAPACITACION'),
(35, '1.', 'Mantiener una esctrcita limpieza e higiene personal y aplica buenas practicas higiénicas en sus labores. ', 'ARTICULO 14 PRACTICAS HIGIENICAS Y MEDIDAS DE PROTECCION'),
(36, '2.', 'Usan vestimenta de trabajo que cumpla los requisitos establecidos. El operador dota de vestimenta de trabajo en número suficiente para el personal manipulador.', 'ARTICULO 14 PRACTICAS HIGIENICAS Y MEDIDAS DE PROTECCION'),
(37, '4.', 'Se lavan y desinfectan las manos cada vez que sea necesario.', 'ARTICULO 14 PRACTICAS HIGIENICAS Y MEDIDAS DE PROTECCION'),
(38, '5.', 'Mantienen el cabello recogido y cubierto totalmente, ', 'ARTICULO 14 PRACTICAS HIGIENICAS Y MEDIDAS DE PROTECCION'),
(39, '6.', 'Dependiendo del riesgo de manipulación asociado con el proceso es obligatorio el uso de tapabocas mientras se manipula el alimento.', 'ARTICULO 14 PRACTICAS HIGIENICAS Y MEDIDAS DE PROTECCION'),
(40, '7.', 'Mantienen las uñas cortas, limpias y sin esmalte.', 'ARTICULO 14 PRACTICAS HIGIENICAS Y MEDIDAS DE PROTECCION'),
(41, '8.', 'No se permiten anillos, aretes, joyas u otros accesorios mientras el personal realice sus labores. ', 'ARTICULO 14 PRACTICAS HIGIENICAS Y MEDIDAS DE PROTECCION'),
(42, '9.', 'Usan calzado cerrado, de material resistente e impermeable, de tacón bajo  y suela antideslizante.', 'ARTICULO 14 PRACTICAS HIGIENICAS Y MEDIDAS DE PROTECCION'),
(43, '10.', 'Cuando se usan guantes, se mantienen limpios, sin roturas o desperfectos y son tratados con el mismo cuidado higiénico de las manos sin protección. ', 'ARTICULO 14 PRACTICAS HIGIENICAS Y MEDIDAS DE PROTECCION'),
(44, '11.', 'No es permitido comer, beber o masticar cualquier objeto o producto, como tampoco fumar o escupir en las áreas de producción o en cualquier otra zona donde exista riesgo de contaminación del alimento.', 'ARTICULO 14 PRACTICAS HIGIENICAS Y MEDIDAS DE PROTECCION'),
(45, '12.', 'El personal que presente afecciones de la piel o enfermedad infectocontagiosa es excluido de toda actividad directa de manipulación de alimentos.', 'ARTICULO 14 PRACTICAS HIGIENICAS Y MEDIDAS DE PROTECCION'),
(46, '13-14', 'Las personas que actúen en calidad de visitantes a las áreas de fabricación cumplen con las medidas de protección y sanitarias estipuladas en el presente capitulo.', 'ARTICULO 14 PRACTICAS HIGIENICAS Y MEDIDAS DE PROTECCION'),
(47, 'Articulo 21', 'Todas  las operaciones de fabricaciòn, procesamiento, envase, almacenamiento y distribución de los alimentos están sujetos a  controles de calidad. Èstos  procedimientos y controles  previenen los defectos evitables y reducen los defectos naturales o inevitables a niveles tales que no representen riesgo a la salud.', 'CAPITULO V ASEGURAMIENTO Y CONTROL DE LA CALIDAD E INOCUIDAD'),
(48, 'Articulo 22 ', 'El sistema de control y aseguramiento de la calidad tiene como mínimo: Especificaciones y criterios de aceptacion- liberacion y/o rechazo sobre las materias primas y productos terminados.  - Llevan formato de control de calidad de productos en bodega, donde  se encuentre como mínimo fecha de vencimiento, lote, características organolépticas, temperatura, peso, fecha de salida de bodega, marca y nombre producto. - cuentan Manuales, guias, procesos que describan sus detalles esenciales del sistema de control de los alimentos. -cuentan con el plan de muestreo que garanticen resultados confiables representativo del lote analizado.', 'CAPITULO V ASEGURAMIENTO Y CONTROL DE LA CALIDAD E INOCUIDAD'),
(49, '1-4', 'El operador cuenta con protocolos para almacenar, señalizar y disponer los productos no conformes y están documentados', 'CAPITULO V ASEGURAMIENTO Y CONTROL DE LA CALIDAD E INOCUIDAD'),
(50, 'Parrafo 1/2', 'El responsable del establecimiento prodra aplicar el sistema de aseguramiento de la inocuidad mediantes analisis de peligros y puntos criticos de control (AAPPCC) el cual debera aplicarlo de acuerdo a los principios gernerales.', 'CAPITULO V ASEGURAMIENTO Y CONTROL DE LA CALIDAD E INOCUIDAD'),
(51, 'Articulo 26 ', 'Se cuenta con un plan de saneamiento con objetivos claramente definidos y con los procedimientos requeridos para disminuir los riesgos de contaminación de los alimentos. El plan de Saneamiento debe estar escrito y a disposiciòn de la autoridad sanitaria competente.', 'CAPITULO VI SANEAMIENTO'),
(52, '1.', 'Programa de Limpieza y Desinfecciòn. Los procedimientos de limpieza y desinfección satisfacen las necesidades particulares del proceso y del producto de que se trate. Cada establecimiento debe tener por escrito todos lo procemientos, incluyendo los agentes y sustancias utilizadas, asi como las concentraciones o formas de uso y los equipos e implementos requeridos para efectuar las operaciones y periodicidicidad de limpieza y desinfección. Verificar Registros, las instalaciones, equipos y utensilios se encuentran limpios y han sido desinfectados,  lo establecido en el programa es ejecutado correctamente en el comedor escolar y bodega ', 'CAPITULO VI SANEAMIENTO'),
(53, '2.', 'Programa de desechos sólidos (basuras): Cuenta con las instalaciones, elementos, áreas, recursos y procedimientos que garanticen una eficiente labor de recolección, conducción, manejo, almacenamiento interno, clasificación, transporte y disposición, lo cual tendrá que hacerse observando las normas de higiene y salud ocupacional establecidas con el proposito de evitar la contaminación de los alimentos, áreas, dependencias y equipos o el deterioro del medio ambiente, definen uso de colores de bolsas y esta correctamente relacionada segun su tipo, registros de evacuación de desechos incluido residuos de aceite . Verificar registros, lo establecido en el programa es ejecutado correctamente.  ', 'CAPITULO VI SANEAMIENTO'),
(54, '3.', 'Programa de control de plagas. Las plagas entendidas como artrópodos y roedores son objeto de un programa de control específico.  Verificar registros, empresa externa, cronograma para el control de plagas, tener en cuenta Decreto 1843 de 1991. verificar si lo establecido en el programa es ejecutado correctamente.', 'CAPITULO VI SANEAMIENTO'),
(55, '4.', 'Establece protocolo de aseguramiento de la calidad del agua, presentando procedimiento del lavado de tanques y certificado de lavado y desinfeccion de tanques.Se realiza muestreo fisicoquimico y/o  microbiologico de calidad de agua ', 'CAPITULO VI SANEAMIENTO'),
(56, 'Articulo 27', 'Las operaciones y condicones de almacenamiento, distribuciòn, transporte y comercializaciòn de alimentos debe evitar: A. La contaminaciòn y alteraciòn del alimento B: La proliferaciòn de microorganismos indeseables en los alimentos y C. El deterioro o daño del envase o embalaje.', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(57, 'Articulo 28-1', 'Se lleva un control de primeras entradas y primeras salidas con el fin de garantizar la rotación de los productos.', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(58, '2.', 'El almacenamiento de productos que requieren refrigeración o congelación se realiza teniendo en cuenta las condiciones de temperatura, humedad y circulación del aire que requiera cada alimento. Se lleva a cabo un control de temperatura y humedad que asegure la conservación del producto. Temperatura de refrigeracion 4°C +/-2°C, la temperatura de congelacion debe ser de -18°C', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(59, '3.', 'El almacenamiento de los insumos y productos terminados se realiza de manera que se minimice su deterioro y se eviten aquellas condiciones que puedan afectar la higiene, funcionalidad e integridad de los mismos. Además se identifican claramente para conocer su procedencia, calidad y tiempo de vida.', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(60, '4.', 'El almacenamiento de los insumos o productos terminados se realiza ordenadamente en pilas o estibas con separación mínima de 60 centímetros con respecto a las paredes perimetrales, y se disponen sobre paletas o tarimas elevadas del piso por lo menos 15 centímetros de manera que se permita la inspección, limpieza y fumigación, si es el caso. No se deben utilizar estibas sucias o deterioradas.', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(61, '5.', 'En los sitios o lugares destinados al almacenamiento de materias primas, envases y productos terminados no se realizan actividades diferentes a éstas.', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(62, '6.', 'El almacenamiento de los alimentos devueltos a la bodega por fecha de vencimiento caducada o producto retenido o cambios, se realiza en un área o depósito exclusivo para tal fin; este depósito está identificado claramente  Y cuenta con un libro de registo o formato en el cuan se consigna fecha, cantidad de producto devuelto, salidas parciales y destino final.', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(63, '7.', 'Los plaguicidas, detergentes, desinfectantes y otras sustancias peligrosas que por necesidades de uso se encuentren dentro de la fábrica, están etiquetadas adecuadamente con un rótulo en que se informe sobre su toxicidad y empleo. Estos productos se almacenan en áreas o estantes especialmente destinados para este fin y su manipulación sólo podrá hacerla el personal idóneo, evitando la contaminación de otros productos. Se encuentran en un area especifica los productos de L&D empleados en las IEO y estos son los productos aprobados?', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(64, 'Articulo 29             ', 'El transporte se realiza en condiciones tales que excluye la contaminación y/o la proliferación de microorganismos y proteje contra la alteración del alimento o los daños del envase. Lleva un sistema de verificacion y registro de Control la temperatura de Thermo King.', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(65, '2.', 'Los alimentos y materias primas que por su naturaleza requieran mantenerse refrigerados o congelados son transportados y distribuidos bajo condiciones que aseguren y garanticen el mantenimiento de las condiciones de refrigeración o congelación hasta su destino final. asegura la cadena de frio.', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(66, '3.', 'Los vehículos que posean sistemas de refrigeración o congelación, son sometidos a revisión periódica, con el fin de que su funcionamiento garantice las temperaturas requeridas para la buena conservación de los alimentos y contarán con indicadores y sistemas de registro de estas temperaturas.', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(67, '4.', 'Se revisa los vehículos antes de cargar los alimentos, con el fin de asegurar que se encuentren en buenas condiciones sanitarias se lleva registros y estos estan consolidados ', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(68, '5.', 'Los vehículos son adecuados para el fin perseguido y fabricados con materiales tales que permitan una limpieza fácil y completa. Igualmente se mantienen limpios y, en caso necesario se someterán a procesos de mantenimiento.', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(69, '6.', 'evitar transportar alimentos con diferente riesgo en salud publica; evitar una contminacion cruzada', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(70, '7', 'Se prohibe disponer de alimentos directamente sobre el suelo de los medios de transporte para este fin se utilizaran los recipientes canastillas o implrmentos de material adecuado de manera que aisle el producto de todo posibilidad de contaminacion.', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(71, '8', 'Se prohibe transportar conjuntamente en un mismo vehículo alimentos con sustancias peligrosas y otras que por su naturaleza representen riesgo de contaminación del alimento o la materia prima.', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(72, '9', 'Los vehículos transportadores de alimentos llevan en su exterior en forma claramente visible la leyenda: Transporte de Alimentos y el logo del  PAE.', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(73, '10', 'Durante las actividades de distribución de alimentos y materias primas toda persona natural o juridica  garantiza el mantenimiento de las condiciones sanitarias y de temperatura de estos. ', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(74, '10.1', 'No existe comunicación entre la unidad de carga y la cabina del conductor', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(75, '10.2', 'El diseño de la unidad de transporte permite la evacuación de las aguas de lavado en caso de que la unidad de transporte tenga orificios para drenaje, estos cuentan con un sistema de cerrado que lo aisle del exterior', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(76, '10.3', 'La unidad transportadora cuenta con recipientes, canastillas y/o implementos de acuerdo a la normatividad sanitaria vigente para el tipo de producto transportado y son de material higienio sanitario, protegiendo el producto de la contaminación y del contacto directo con el piso y otras superficies del vehiculo', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(77, '10.4', 'Los recipientes, canastilas y/o implementos que entran en contacto con el producto son mantenidos de forma que se evita la contaminacion con el alimento,  son de facil limpieza y desinfección se lleva registros de lavado de canastillas en bodega', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(78, '10.5', 'Se cuenta con valoración del medico ocupacional al personal manipulador', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(79, '10.6', 'Los manipuladores de alimentos cumplen con las prácticas necesarias durante el transporte y la manipulación.', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(80, '10.7', 'El personal manipulador de alimentos cuenta con la dotación y vestimenta de trabajo acorde con la actividad.', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(81, '10.8', 'En caso de observarse descargue de productos, los manipuladores de alimentos se lavan con agua y jabón desinfectante las manos.', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(82, '10.9', 'El manipulador recibe capacitación continua y permantente acorde a la actividad que realice: manipulacion de alimentos (BPM,higiene, Limpieza locativa , Almacenamiento, Calidad, higiene personal, higiene vehiculo, prevención de contaminación cruzada, control de temperatura)', 'CAPITULO VII ALMACENAMIENTO - DISTRIBUCIÓN Y TRANSPORTE DE ALIMENTOS Y MATERIAS PRIMAS'),
(83, 'Anexo Tecnico ', 'El operador establece un area para muestras y contramuestras de productos industrializados, estos están correctamente rotulados (con fecha de toma y de eliminación, hora de toma, lote, Número de menú, modalidad, temperatura de toma, y persona responsable del proceso.)  y se llevan registros de su recepcion y desecho  ', 'PROGRAMA DE MUESTREO FISICOQUIMICO Y MICROBIOLOGICO'),
(84, 'Anexo Tecnico ', 'Se presenta el programa de mantenimiento preventivo correctivo y de calibracion con protocolos, procedimientos y cronogramas consolidando e inventariando junto a las hojas de vida, los equipos e instrumentos de medicion ', 'PROGRAMA DE MANTENIMIENTO PREVENTIVO Y CORRECTIVO E CALIBRACION DE EQUIPOS  E INSTRUMENTOS DE MEDICI'),
(85, 'Anexo Tecnico ', 'El operador acredita laboratorio externo o empresa certificada con certificados de calibración de los equipos e instrumentos de medicion', 'PROGRAMA DE MANTENIMIENTO PREVENTIVO Y CORRECTIVO E CALIBRACION DE EQUIPOS  E INSTRUMENTOS DE MEDICI'),
(86, 'Anexo Tecnico ', 'El operador presenta plan de capacitación a manipuladores y  operarios desde su vinculacion y son sometidos a capacitación, actualización continua y permanente ', 'PROGRAMA DE CAPACITACION CONTINUA PARA OPERARIOS Y MANIPULADORAS'),
(87, 'Anexo Tecnico ', 'Presenta cronograma de capacitacion, define temas minimos  y se llevan registros', 'PROGRAMA DE CAPACITACION CONTINUA PARA OPERARIOS Y MANIPULADORAS'),
(88, 'Anexo Tecnico ', 'El operador presenta programa de proveedores, estableciendo aspectos y criterios de evaluación, aceptación y seguimiento a proveedores, este contiene las especificaciones de calidad, criterios de aceptación y rechazo de las materias primas e insumos, condiciones de recibo, almacenamiento, uso y controles de calidad, así como la caracterización de materias primas e insumos y su rotación, aplicacion  del sistema PEPS (Primero en Entrar, Primero en Salir), requisitos de rotulado de acuerdo con la reglamentación sanitaria vigente (Resoluciones 5109 de 2005, 333 de 2011 y 810 de 2021) y el oportuno seguimiento de los mismos a partir de los registros de control.', 'PROVEEDORES, MATERIAS PRIMAS E INSUMOS'),
(89, 'Anexo Tecnico ', 'El operador acredita como minimo 1 visita a proveedores. Incluye formato de visita técnica a la planta o bodega del proveedor, controles criterios tecnicos y cronogramas ', 'PROVEEDORES, MATERIAS PRIMAS E INSUMOS');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `preguntas_infraestructura`
--

CREATE TABLE `preguntas_infraestructura` (
  `id_pregunta` int(11) NOT NULL,
  `numero` varchar(50) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `categoria` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `preguntas_infraestructura`
--

INSERT INTO `preguntas_infraestructura` (`id_pregunta`, `numero`, `descripcion`, `categoria`) VALUES
(1, '1.1', 'La unidad de servicio se encuentra aislada de focos de insalubridad, en un lugar fuera de riesgos de inundacion u otra situación atribuible al medio ambiente.', 'infraestructura'),
(2, '1.2', 'Existe separación física de las areas de almacenamiento, preparación, distrIbución y servicios sanitarios.', 'infraestructura'),
(3, '1.3', 'Se encuentra identificada la ruta de evacuacion, las salidas de emergencia y los punto de encuentro en todas las áreas del comedor.', 'infraestructura'),
(4, '1.4', 'Se cuenta con servicio de lavado de manos para los titulares de derecho y esta en buen estado.', 'infraestructura'),
(5, '2.1', 'Existe área de preparación. Especificar área en M².', 'area de preparacion de alimentos'),
(6, '2.2', 'Las paredes del área son lisas y de fácil limpieza y desinfección, sin presencia de humedad.', 'area de preparacion de alimentos'),
(7, '2.3', 'El piso del área de preparación ésta construido en material de fácil limpieza y desinfección, sin presencia de grietas u orificios. ', 'area de preparacion de alimentos'),
(8, '2.4', 'El techo del área de preparación ésta construido en material de fácil limpieza y desinfección, sin presencias de humedad ni goteras.', 'area de preparacion de alimentos'),
(9, '2.5', 'Los mesones para preparar los alimentos son de material de fácil limpieza y desinfección. Enuncie el material y el estado de los mesones.', 'area de preparacion de alimentos'),
(10, '2.6', 'Cuenta con sifones y rejillas anticucarachas. Específique el estado.', 'area de preparacion de alimentos'),
(11, '2.7', 'Cuenta con lavaplatos y suministro de agua. Específique el estado.', 'area de preparacion de alimentos'),
(12, '2.8', 'Las ventanas que se comunican con el medio exterior se encuentran provistas de mallas antinsectos de fácil limpieza.', 'area de preparacion de alimentos'),
(13, '2.9', 'Cuenta con ventilación en las áreas de preparación.', 'area de preparacion de alimentos'),
(14, '2.10', 'Cuenta con lámparas, y bombillos y están debidamente protegidos en caso de ruptura. ', 'area de preparacion de alimentos'),
(15, '2.11', 'Las  instalaciones eléctricas  del  servicio se encuentran protegidas y ubicadas adecuadamente.', 'area de preparacion de alimentos'),
(16, '3.1', 'Existe área de almacenamiento. Especificar área en M².', 'area de almacenamiento de alimentos'),
(17, '3.2', 'Las paredes del área son lisas y de fácil limpieza y desinfección, sin presencia de humedad.', 'area de almacenamiento de alimentos'),
(18, '3.3', 'El piso del área de almacenamiento ésta construido en material de fácil limpieza y desinfección, sin presencias de grietas u orificios. ', 'area de almacenamiento de alimentos'),
(19, '3.4', 'El techo del área de almacenamiento ésta construido en material de fácil limpieza y desinfección, sin presencias de humedad ni goteras.', 'area de almacenamiento de alimentos'),
(20, '3.5', 'Las ventanas que se comunican con el medio exterior se encuentran provistas de mallas antinsectos  de fácil limpieza y desinfección.', 'area de almacenamiento de alimentos'),
(21, '3.6', 'El área de almacenamiento cuenta con ventilación.', 'area de almacenamiento de alimentos'),
(22, '3.7', 'Se cuenta con anaqueles, recipientes debidamente marcados y tapados, estantes o mesones  para almacenar los alimentos de manera adecuada en material de fácil limpieza que no permitan la contaminación.', 'area de almacenamiento de alimentos'),
(23, '3.8', 'Se cuenta con estibas o canastilla base limpias para almacenar los alimentos, en material de fácil limpieza que no permita la contaminación.', 'area de almacenamiento de alimentos'),
(24, '3.9', 'Cuenta con lámparas, bombillos y están  debidamente protegidos en caso de ruptura.', 'area de almacenamiento de alimentos'),
(25, '3.10', 'Las  instalaciones eléctricas  del  servicio se encuentran protegidas y ubicadas adecuadamente.', 'area de almacenamiento de alimentos'),
(26, '4.1', 'Existe área de distribución. Especifique área en M².', 'area de distribucion de alimentos'),
(27, '4.2', 'El piso del área de distribución ésta construido en material de fácil limpieza y desinfección, sin presencias de grietas u orificios. ', 'area de distribucion de alimentos'),
(28, '4.3', 'El techo del área de distribución ésta construido en material de fácil limpieza y desinfección.', 'area de distribucion de alimentos'),
(29, '4.4', 'El área del comedor cuenta con ventilación.', 'area de distribucion de alimentos'),
(30, '4.5', 'El área del comedor cuenta con iluminación.', 'area de distribucion de alimentos'),
(31, '4.6', 'El área del comedor cuenta con sillas. Específique Nro de sillas, material y estado.', 'area de distribucion de alimentos'),
(32, '4.7', 'El área del comedor cuenta con mesas. Específique Nro de mesas, material y estado.', 'area de distribucion de alimentos'),
(33, '4.8', 'Las  instalaciones eléctricas  del  servicio se encuentran protegidas y ubicadas adecuadamente.', 'area de distribucion de alimentos'),
(34, '5.1', 'Las instalaciones sanitarias se encuentran en buen estado y funcionando (lavamanos e inodoro).', 'instalaciones sanitarias y de aseo'),
(35, '5.2', 'La ubicación de los servicios sanitarios son aislados del area de preparación o distribución.', 'instalaciones sanitarias y de aseo'),
(36, '5.3', 'Existen puertas que permitan el aislamiento de las instalaciones sanitarias de las demás áreas.', 'instalaciones sanitarias y de aseo'),
(37, '5.4', 'Cuenta con área de vestier para el personal manipulador.', 'instalaciones sanitarias y de aseo'),
(38, '5.5', 'Cuenta con área especifica de almacenamiento de los elementos de aseo del servicio, y esta identificada.', 'instalaciones sanitarias y de aseo'),
(39, '5.6', 'Cuenta con area especifica de lavado de los elementos de aseo del servicio.', 'instalaciones sanitarias y de aseo'),
(40, '6.1', 'Cuenta con servicio de agua potable y / o aseguramiento de la misma.', 'servicios publicos'),
(41, '6.2', 'Cuenta con tanque de almacenamiento de agua, en que material y en que condiciones se encuentra.', 'servicios publicos'),
(42, '6.3', 'Cuenta con servicios de energía permanente.', 'servicios publicos'),
(43, '6.4', 'Cuenta con servicio de alcantarillado.', 'servicios publicos'),
(44, '6.5', 'Cuenta con servicio de recolección de basuras.', 'servicios publicos'),
(45, '6.6', 'Cuenta con servicio de gas. Específique de que tipo, pipeta o gas natural (la ubicación de la pipeta de gas es adecuada apartada de fuente de calor, en área ventilada y protegida).', 'servicios publicos'),
(46, '7.1', 'Especifique el N° de cucharas, material y estado.', 'dotacion de menaje'),
(47, '7.4', 'Especifique el N° de platos, material y estado.', 'dotacion de menaje'),
(48, '7.6', 'Especifique el N° de vasos, material y estado.', 'dotacion de menaje'),
(49, '7.7', 'Especifique el N° de bandejas, material y estado.', 'dotacion de menaje'),
(50, '7.8', 'Especifique el N° de ollas, capacidad y estado.', 'dotacion de menaje'),
(51, '7.9', 'Especifique el N° de canecas plasticas, capacidad y estado.', 'dotacion de menaje'),
(52, '7.10', 'Especifique el N° de jarras plasticas, capacidad y estado.', 'dotacion de menaje'),
(53, '7.11', 'Especifique el N° de baldes, capacidad y estado.', 'dotacion de menaje'),
(54, '7.12', 'Especifique el N° de cucharas para servir, material y estado.', 'dotacion de menaje'),
(55, '7.13', 'Especifique el N° de pailas capacidad y estado.', 'dotacion de menaje'),
(56, '7.14', 'Especifique el N° de cuchillos para cocina, material y estado.', 'dotacion de menaje'),
(57, '7.15', 'N° de neveras. Especifique capacidad en litros, estado y termometro en la casilla de observaciones.', 'dotacion de menaje'),
(58, '7.16', 'N° de refrigeradores y/o congeladores. Especifique capacidad, estado y termometro en la casilla de observaciones.', 'dotacion de menaje'),
(59, '7.18', 'Nº de estufas lineales, caracteristicas y estado.', 'dotacion de menaje'),
(60, '7.19', 'Gramera.', 'dotacion de menaje'),
(61, '7.20', 'Nº de licuadoras, capacidad en litros.', 'dotacion de menaje'),
(62, '7.21', 'Termometro.', 'dotacion de menaje'),
(63, '7.22', 'N° de balanzas 25 lbs. Capacidad y estado.', 'dotacion de menaje'),
(64, '8.', 'Otros, cuales: ', 'dotacion de menaje'),
(65, '8.2', 'Cernidores.', 'dotacion de menaje'),
(66, '8.3', 'Que tipo de material se utiliza para la limpieza y secado de utensilios de cocina.', 'dotacion de menaje');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `preguntas_tecnica`
--

CREATE TABLE `preguntas_tecnica` (
  `id_tecnica` int(11) NOT NULL,
  `numero` int(11) NOT NULL,
  `preguntas` text NOT NULL,
  `categorias` varchar(255) DEFAULT NULL,
  `tipo_racion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `preguntas_tecnica`
--

INSERT INTO `preguntas_tecnica` (`id_tecnica`, `numero`, `preguntas`, `categorias`, `tipo_racion`) VALUES
(1, 1, 'La unidad de servicio esta ubicada en un lugar alejado de focos de insalubridad, maleza y aguas estancadas.', 'Edificacion e instalaciones', 'Preparado en Sitio\r'),
(2, 2, 'Los techos, paredes y pisos se encuentran en buen estado.', 'Edificacion e instalaciones', 'Preparado en Sitio\r'),
(3, 3, 'Las puertas se encuentran protegidas para evitar  el ingreso  y refugio de plagas, las aberturas entre las puertas exteriores y los pisos no deben ser mayores a 1 cm. ', 'Edificacion e instalaciones', 'Preparado en Sitio\r'),
(4, 4, 'Los mesones empleados en el manejo y preparacion de alimentos se encuentran en buen estado.', 'Edificacion e instalaciones', 'Preparado en Sitio\r'),
(5, 5, 'Las lamparas o bombillos se encuentran protegidas y funcionando. ', 'Edificacion e instalaciones', 'Preparado en Sitio\r'),
(6, 6, 'No se evidencian instalaciones electricas expuestas en la zona de preparacion', 'Edificacion e instalaciones', 'Preparado en Sitio\r'),
(7, 7, 'Los sifones y drenajes se encuentran en buen estado, protegidos (rejilla anticucarachas), funcionando y limpios.', 'Edificacion e instalaciones', 'Preparado en Sitio\r'),
(8, 8, 'Las ventanas y aberturas que se comuniquen con el ambiente exterior estan provistas con malla anti-insecto resistentes, de facil limpieza y bien conservadas.', 'Edificacion e instalaciones', 'Preparado en Sitio\r'),
(9, 9, 'La institucion educativa cuenta con comedor  para el consumo de los alimentos.', 'Edificacion e instalaciones', 'Preparado en Sitio\r'),
(10, 10, 'El comedor escolar o espacio destinado cuenta con las mesas y sillas de acuerdo al turno atendido y se encuentran en buen estado.', 'Edificacion e instalaciones', 'Preparado en Sitio\r'),
(11, 11, 'Se cuenta con un area de almacenamiento protegida e iluminada, con ventilacion natural o artificial.', 'Edificacion e instalaciones', 'Preparado en Sitio\r'),
(12, 12, 'El area de almacenamiento de las materias primas es acorde a la capacidad de los cupos atendidos.', 'Edificacion e instalaciones', 'Preparado en Sitio\r'),
(13, 13, 'Esta constituido en la  institucion educativa el comite de alimentacion escolar (CAE). Cuenta con acta de conformacion.', 'Edificacion e instalaciones', 'Preparado en Sitio\r'),
(14, 14, 'La institucion educativa cuenta con acta de reunion bimensual del comite de alimentacion escolar (CAE). ', 'Edificacion e instalaciones', 'Preparado en Sitio\r'),
(15, 15, 'La institucion educativa cuenta con servicio de gas propano (dos cilindros 1 de 100lb y 1 de 40lb uno en uso y el otro en reserva cargado) ', 'Area de Almacenamiento', 'Preparado en Sitio\r'),
(16, 16, 'Los productos o materias primas se encuentran adecuadamente almacenados e identificados y en caso de tener jornada unica esten almacenados de acuerdo a la modalidad. ', 'Area de Almacenamiento', 'Preparado en Sitio\r'),
(17, 17, 'Se evidencian alimentos libres de algun tipo de contaminacion.', 'Area de Almacenamiento', 'Preparado en Sitio\r'),
(18, 18, 'Se lleva un control de contramuestras de productos de alto riesgo para la salud (solo aplica para los dos sedes educativas designadas por cada operador)', 'Area de Almacenamiento', 'Preparado en Sitio\r'),
(19, 19, 'El area de almacenamiento se mantiene limpia y ordenada.', 'Area de Almacenamiento', 'Preparado en Sitio\r'),
(20, 20, 'Se lleva un control de primeras entradas y primeras salidas con el fin de garantizar la rotacion de los productos.', 'Area de Almacenamiento', 'Preparado en Sitio\r'),
(21, 21, 'Existe recipientes de almacenamiento de agua adecuados y protegidos con tapa, con la capacidad suficiente para atender como minimo las necesidades correspondientes a un dia de preparacion, si usan recipientes cuentan con registro de limpieza y desinfeccion diligenciado.', 'Area de Almacenamiento', 'Preparado en Sitio\r'),
(22, 22, 'Se evidencia registro semanal de prueba de calidad del agua, con el kit basico test de PH y cloro residual en las sedes educativas oficiales', 'Area de Almacenamiento', 'Preparado en Sitio\r'),
(23, 23, 'Se cuenta con recipientes para la disposicion de residuos solidos apropiados con tapa y son removidos con frecuencia. \nNota: Segun  Resolucion 2148 de 2019. Bolsa  blanca para residuos aprovechables (plastico, carton vidrio, papel, metales),  bolsa verde para residuos organicos aprovechables (restos de comida y desechos agricolas) y bolsa negra para los residuos no aprovechables (servilletas, papeles y cartones contaminados con comida y papeles metalizados)', 'Requisitos higienicos ', 'Preparado en Sitio\r'),
(24, 24, 'La preparacion de los alimentos se realiza cumpliendo con lo estipulado en el plan de saneamiento (limpieza y desinfeccion, manejo de residuos, abastecimiento de agua y manejo integral de plagas).', 'Requisitos higienicos ', 'Preparado en Sitio\r'),
(25, 25, 'Los pisos, paredes, techos, mesones de las areas de preparacion, distribucion y consumo se encuentran limpios para garantizar condiciones higienico-sanitarias.', 'Requisitos higienicos ', 'Preparado en Sitio\r'),
(26, 26, 'Todo equipo y utensilio que haya entrado en contacto con materias primas o con material contaminado se limpia y desinfecta cuidadosamente antes de ser nuevamente utilizado.', 'Requisitos higienicos ', 'Preparado en Sitio\r'),
(27, 27, 'Existen letreros alusivos a la aplicacion de BPM, en buen estado y ubicados en las instalaciones del comedor escolar.', 'Requisitos higienicos ', 'Preparado en Sitio\r'),
(28, 28, 'Se evidencia en el comedor escolar la implementacion de una ruta de evacuacion caracterizada a la unidad de servicio de los desechos solidos y liquidos.', 'Requisitos higienicos ', 'Preparado en Sitio\r'),
(29, 29, 'Se dispone de recipiente identificado para la recoleccion de aceite de cocina usado con area destinada para tal fin y se llevan el formato para su contabilizacion', 'Requisitos higienicos ', 'Preparado en Sitio\r'),
(30, 30, 'Se evidencian que las diferentes areas que conforman el comedor escolar estan  identificadas y señalizadas con avisos elaborados en material lavable, resistente y se encuentran en buen estado.', 'Requisitos higienicos ', 'Preparado en Sitio\r'),
(31, 31, 'La Institucion Educativa cuenta con concepto higienico sanitario favorable o favorable con requerimientos o solicitud de visita por parte del operador para realizar visita por secretaria de salud.', 'Requisitos higienicos ', 'Preparado en Sitio\r'),
(32, 32, 'Los productos se encuentran con fecha de vencimiento vigente y son aptos para el consumo.', 'Caracteristicas de calidad de los alimentos.', 'Preparado en Sitio\r'),
(33, 33, 'Los productos utilizados en la unidad de servicio para la preparacion son avalados por el Eje de Calidad e Inocuidad y Alimentacion Saludable', 'Caracteristicas de calidad de los alimentos.', 'Preparado en Sitio\r'),
(34, 34, 'Se lleva registro de temperatura de los alimentos preparados en sitio : \ncontrol de temperatura 2 veces durante el tratamiento termico de la preparacion (minimo 75º C) y al inicio de la distribucion a los titulares de derecho (Minimo 65 ºC).', 'Caracteristicas de calidad de los alimentos', 'Preparado en Sitio\r'),
(35, 35, 'Se evidencia que el alimento a servir se encuentra a temperatura igual o mayor a 65°C.', 'Caracteristicas de calidad de los alimentos', 'Preparado en Sitio\r'),
(36, 36, 'Se evidencia formato de remision de entrega por nivel escolar, con fecha, hora de entrega, debidamente firmado y las cantidades relacionadas en la remision son acordes a la focalizacion designada.', 'Caracteristicas de calidad de los alimentos', 'Preparado en Sitio\r'),
(37, 37, 'Se evidencia entrega de la racion alimentaria designada al personal manipulador de alimentos.', 'Caracteristicas de calidad de los alimentos', 'Preparado en Sitio\r'),
(38, 38, 'El inventario de los productos o materia prima estan acorde a los cupos focalizados y nivel escolar.', 'Caracteristicas de calidad de los alimentos', 'Preparado en Sitio\r'),
(39, 39, 'Se garantiza cumplimiento al rotulado y etiquetado de todos los alimentos suministrados de manera que en los empaques y envases aparezca la siguiente informacion: nombre del alimento, ingredientes, informacion nutricional, contenido neto, peso escurrido, nombre y direccion del fabricante, pais de origen, identificacion del lote, fecha de vencimiento y/o de duracion minima e instrucciones para conservacion, instrucciones de uso, y que las materias primas de calidad cumplan con las especificaciones tecnicas descritas en la resolucion 00335/21, con registro sanitario INVIMA (Resolucion 5109 del 2005, 810 del 2021, 2492 del 2022)', 'Caracteristicas de calidad de los alimentos', 'Preparado en Sitio\r'),
(40, 40, 'Los productos cumplen con las caracteristicas organolepticas y fisicas requeridas, En caso de suministrarse fruta porcionada, la cual por su composicion quimica presente reacciones de pardeamiento enzimatico (banano, manzana, pera), el operador debera garantizar procedimientos no quimicos para evitar esta alteracion en sus caracteristicas organolepticas.', 'Caracteristicas de calidad de los alimentos', 'Preparado en Sitio\r'),
(41, 41, 'Los alimentos altamente perecederos (proteina, lacteos o alimentos de alto riesgo) se encuentran almacenados y refrigerados a temperatura que garantice su conservacion (entre 0 a 4° C) en refrigeracion y (temperaturas inferior a 0°C) en congelacion, y se evidencia registro de temperatura minimo una vez al dia', 'Caracteristicas de calidad de los alimentos', 'Preparado en Sitio\r'),
(42, 42, 'Se evidencian las guias de preparacion en la unidad de servicio y se encuentran ajustadas al ciclo de menu.', 'Caracteristicas de calidad de los alimentos', 'Preparado en Sitio\r'),
(43, 43, 'Los alimentos son preparados acorde con las guias de preparacion estipuladas', 'Caracteristicas de calidad de los alimentos', 'Preparado en Sitio\r'),
(44, 44, 'Los cortes de carne empleados para la preparacion de los menu son acordes a lo establecido por la SED  (Res (caderita, centro de pierna, bola negra) cerdo (brazo y pierna) y pollo (filete de pechuga de pollo sin marinar / pechuga sin piel, sin hueso y sin marinar/ pechuga con piel y hueso sin marinar por beneficiario se debera calcular con base al 65% de parte comestible).', 'Caracteristicas de calidad de los alimentos', 'Preparado en Sitio\r'),
(45, 45, 'Las reposiciones realizadas al operador por causa de baja calidad, deterioro o daño fisico, lotes, fecha de produccion y vencimiento, son resueltas de manera inmediata.', 'Caracteristicas de calidad de los alimentos', 'Preparado en Sitio\r'),
(46, 46, 'Se evidencia formato de reposicion o entrega de faltante de acuerdo a formato establecido por la SED', 'Caracteristicas de calidad de los alimentos', 'Preparado en Sitio\r'),
(47, 47, 'Se evidencia la reposicion o entrega de faltante segun sea el caso (reposicion o faltante) y el diligenciamiento del formato. ', 'Caracteristicas de calidad de los alimentos', 'Preparado en Sitio\r'),
(48, 48, 'Para las I.E  se evidencia  registro de control de temperatura en la recepcion de los alimentos altamente perecederos (res, cerdo y pollo).\n', 'Caracteristicas de calidad de los alimentos', 'Preparado en Sitio\r'),
(49, 49, 'El operador garantiza la inocuidad de los alimentos, evitando la contaminacion cruzada en las diferentes etapas (Almacenamiento, Preparacion y distribucion)', 'Caracteristicas de calidad de los alimentos', 'Preparado en Sitio\r'),
(50, 50, 'La unidad de servicio cuenta con la cantidad de manipuladora(e)s necesarios de acuerdo al numero de raciones o de acuerdo a lo aprobado por la SED\n', 'Personal manipulador de alimentos', 'Preparado en Sitio\r'),
(51, 51, 'La presentacion personal de los manipuladores es adecuada (uñas cortas, limpias y sin esmalte, cabello recogido, sin uso de joyas u otros accesorios ni maquillaje).', 'Personal manipulador de alimentos', 'Preparado en Sitio\r'),
(52, 52, 'El personal manipulador cuenta con la documentacion requerida: certificados medicos, cronograma de capacitaciones (minimo 10 horas), copia de la entrega de dotacion. Debidamente organizada y archivada en la unidad de servicio.', 'Personal manipulador de alimentos', 'Preparado en Sitio\r'),
(53, 53, 'Se evidencia registro de capacitacion en Salud Ocupacional y el personal manipulador de alimentos tiene conocimiento del tema', 'Personal manipulador de alimentos', 'Preparado en Sitio\r'),
(54, 54, 'Se evidencia registro de capacitacion continua en aspectos de BPM (higiene personal y locativa) y el personal manipulador de alimentos posee conocimientos en el tema', 'Personal manipulador de alimentos', 'Preparado en Sitio\r'),
(55, 55, 'Se evidencia registro de capacitacion en preparacion de alimentos y el personal manipulador de alimentos demuestra conocimiento del tema', 'Personal manipulador de alimentos', 'Preparado en Sitio\r'),
(56, 56, 'El personal manipulador cuenta con certificado de capacitacion en manipulacion de alimentos o plan de capacitacion y listado de asistencia.', 'Personal manipulador de alimentos', 'Preparado en Sitio\r'),
(57, 57, 'Se evidencia registro de capacitacion en minuta patron, ciclo de menu y conoce del tema', 'Personal manipulador de alimentos', 'Preparado en Sitio\r'),
(58, 58, 'Se evidencia registro de capacitacion en manejo y diligenciamiento de formatos (plan de saneamiento, entradas y salidas, formato de faltantes, formatos de registro de temperaturas)', 'Personal manipulador de alimentos', 'Preparado en Sitio\r'),
(59, 59, 'Se evidencia registro de capacitacion en estandarizacion de porciones y servido de alimentos.', 'Personal manipulador de alimentos', 'Preparado en Sitio\r'),
(60, 60, 'Se evidencia registro de capacitacion en plan de saneamiento y conoce del tema', 'Personal manipulador de alimentos', 'Preparado en Sitio\r'),
(61, 61, 'El personal manipulador cuenta con el uniforme completo (pantalon blanco, camisa o bata blancos, zapatos antideslizantes cerrados blancos y delantal plastico) y usan elementos de proteccion personal (gorro, tapa bocas y guantes en caso de ser necesario).', 'Personal manipulador de alimentos', 'Preparado en Sitio\r'),
(62, 62, 'Se exige al personal externo que visite las areas de almacenamiento, preparacion y/o participe en la distribucion de alimentos de los comedores escolares, el uso de la dotacion y el cumplimiento de las practicas de higiene y de manipulacion de alimentos establecidas en la normatividad sanitaria vigente. ', 'Personal manipulador de alimentos', 'Preparado en Sitio\r'),
(63, 63, 'Se evidencia que se cumple con la modalidad contratada', 'Ciclo de minuta', 'Preparado en Sitio\r'),
(64, 64, 'Se evidencia publicado ciclo de menu con dimensiones 64cm x 46cm establecidas por la SED, QR de atencion al ciudadano, ademas se debe evidenciar la publicacion del Noti PAE con linea telefonica y correo electronico de contacto del operador para la atencion de las PQRS.', 'Ciclo de minuta', 'Preparado en Sitio\r'),
(65, 65, 'Se da cumplimiento al menu del dia', 'Ciclo de minuta', 'Preparado en Sitio\r'),
(66, 66, 'Se cumple con el peso servido de acuerdo al ciclo de menu por nivel escolar.', 'Ciclo de minuta', 'Preparado en Sitio\r'),
(67, 67, 'Se evidencia la lista de intercambios en el comedor escolar', 'Ciclo de minuta', 'Preparado en Sitio\r'),
(68, 68, 'Se evidencia la ficha tecnica de informacion del PAE aprobado y publicado en un lugar visible.', 'Ciclo de minuta', 'Preparado en Sitio\r'),
(69, 69, 'Se evidencia el cumplimiento del manual de imagen en la documentacion (formatos, avisos, informes, procedimientos e instructivos) ', 'Ciclo de minuta', 'Preparado en Sitio\r'),
(70, 70, 'El horario de consumo de los alimentos se encuentra publicado en un lugar visible del comedor escolar', 'Horario del consumo de alimentos', 'Preparado en Sitio\r'),
(71, 71, 'Se evidencia que se cumple con los horarios de consumo de los alimentos (Los cambios de horarios deben ser aprobados previamente por el CAE y debe constar acta firmada). ', 'Horario del consumo de alimentos', 'Preparado en Sitio\r'),
(72, 72, 'Se evidencia Plan de Saneamiento en tamaño adecuado de letra, acorde a  la Unidad de Servicio, cumpliendo con los programas: limpieza y desinfeccion, control de plagas, desechos solidos y abastecimiento o suministro de agua.', 'Plan de Saneamiento', 'Preparado en Sitio\r'),
(73, 73, 'Se lleva Registro de Limpieza y desinfeccion diligenciado de acuerdo al Plan de Saneamiento.', 'Plan de Saneamiento', 'Preparado en Sitio\r'),
(74, 74, 'Se garantiza que los equipos para el almacenameinto de los alimentos y utensilios se encuentran en adecuadas condiciones de limpieza y desinfeccion.', 'Plan de Saneamiento', 'Preparado en Sitio\r'),
(75, 75, 'Se evidencia certificado de control de plagas en la unidad de servicio vigente.', 'Plan de Saneamiento', 'Preparado en Sitio\r'),
(76, 76, 'Se observa registros de las actividades realizadas y tipo de sustancias empleadas ', 'Plan de Saneamiento', 'Preparado en Sitio\r'),
(77, 77, 'Se evidencia el formato para el registro semanal de las actividades para control de plagas debidamente diligenciado. ', 'Plan de Saneamiento', 'Preparado en Sitio\r'),
(78, 78, 'Se evidencia cronograma para el control de plagas en el comedor escolar (fumigacion, desratizacion y desinsectacion) y se cumple con el mismo.', 'Plan de Saneamiento', 'Preparado en Sitio\r'),
(79, 79, 'Las instalaciones y/o alimentos se encuentran libres de daños causados por plagas o roedores (ratas, hormigas, palomas, cucarachas, etc.).', 'Plan de Saneamiento', 'Preparado en Sitio\r'),
(80, 80, 'Se garantiza el adecuado almacenamiento de los elementos y sustancias de limpieza y desinfeccion en contenedores y las areas establecidas con hoja o carta de seguridad, debidamente identificadas evitando el contacto con las materias primas, alimentos preparados, utensilios y menaje.', 'Plan de Saneamiento', 'Preparado en Sitio\r'),
(81, 81, 'Se evidencia que las materias primas crudas tales como  verduras, hortalizas, frutas y huevos se lavan y/o desinfectan antes de su preparacion.', 'Plan de Saneamiento', 'Preparado en Sitio\r'),
(82, 82, 'El transporte garantiza el mantenimiento de las condiciones de conservacion requeridas por el producto alimentario: refrigeracion, congelacion, recipientes o canastillas de material sanitario con tapa, etc., y cumple con la normatividad vigente. (Resolucion 2505 de 2004), no se transportan conjuntamente en un mismo vehiculo alimentos o materias primas con sustancias peligrosas y otras sustancias que por su naturaleza representen riesgo de contaminacion del alimento o la materia prima (incluye productos de aseo y pipas de gas)', 'Transporte de alimentos', 'Preparado en Sitio\r'),
(83, 83, 'Las materias primas son transportadas en canastillas plasticas limpias. el transportador deja copia del registro del previo lavado y desinfecion de las mismas desde la bodega hasta las Institucion Educativa Oficial.', 'Transporte de alimentos', 'Preparado en Sitio\r'),
(84, 84, 'Los vehiculos se encuentran en adecuadas condiciones sanitarias, de aseo y operacion para el transporte de los alimentos.', 'Transporte de alimentos', 'Preparado en Sitio\r'),
(85, 85, 'El vehiculo tiene concepto sanitario favorable, formato de limpieza y desinfeccion del vehiculo y formulario de inscripcion sanitaria para vehiculos transportadores de alimentos y bebidas.', 'Transporte de alimentos', 'Preparado en Sitio\r'),
(86, 86, 'El transporte de alimentos cuenta con aviso del Programa de Alimentacion Escolar (PAE).', 'Transporte de alimentos', 'Preparado en Sitio\r'),
(87, 87, 'El transportador (conductor y ayudante) cuenta con registro de capacitacion continua en aspectos de BPM  segun anexo 24, examen medico-ocupacional, vestimenta limpia y adecuada (elementos de proteccion personal), de acuerdo a la normatividad vigente.', 'Transporte de alimentos', 'Preparado en Sitio\r'),
(88, 88, 'El personal manipulador puede verificar la cantidad de materia prima recepcionada, ya sea con bascula en la IOE o vehiculo.', 'Transporte de alimentos', 'Preparado en Sitio\r'),
(89, 89, 'Los equipos (estufa, licuadora, equipo de frio),  utilizados en la preparacion se encuentran funcionando adecuadamente y cuentan con hoja de vida.', 'Equipo y utensilios ', 'Preparado en Sitio\r'),
(90, 90, 'Los equipos de medicion (gramera, termometro y balanza) cuentan con registro de verificacion de masa y temperatura.', 'Equipo y utensilios ', 'Preparado en Sitio\r'),
(91, 91, 'Las neveras, congeladores y demas equipos de almacenamiento cuentan con registro de temperatura (minimo una vez al dia)', 'Equipo y utensilios ', 'Preparado en Sitio\r'),
(92, 92, 'Los utensilios tales como tablas, cucharas, ollas y demas menaje estan fabricados con materiales sanitarios, resistentes a la corrosion de facil limpieza y desinfeccion y se encuentran en buen estado.', 'Equipo y utensilios ', 'Preparado en Sitio\r'),
(93, 93, 'Se cuenta con los equipos y utensilios minimos requeridos para la prestacion del servicio segun modalidad ', 'Equipo y utensilios ', 'Preparado en Sitio\r'),
(94, 94, 'El operador garantiza como minimo el 60% del menaje (platos, vasos, cucharas) y equipos  (nevera, estufa, licuadora y congelador) correspondientes a lo focalizado en la IEO  y se evidencia la relacion en la carpeta tecnica.', 'Equipo y utensilios ', 'Preparado en Sitio\r'),
(95, 95, 'Se evidencia dotacion de los elementos de higiene personal (jabon liquido antibacterial inoloro, papel higienico).', 'Insumos e implementos de aseo', 'Preparado en Sitio\r'),
(96, 96, 'Se evidencia que los implementos de limpieza y desinfeccion (desinfectante liquido, detergente biodegradable para el lavado de platos inoloro, esponja de fibra abrasiva media, limpiones en microfibra, toallas absorbentes, jabon de aseo general inoloro, bolsas plasticas de color blanco, verde y negro, esponja plastica para el lavado de ollas, escoba, trapero y  recogedor) se encuentran en la cantidad requerida de acuerdo al cupo atendido  para complemento alimentario y jornada unica, segun corresponda en la unidades de servicio especificados en la resolucion 335 del 23 de diciembre del 2021.', 'Insumos e implementos de aseo', 'Preparado en Sitio\r'),
(97, 97, 'Los implementos de aseo  permanecen almacenados en lugares separados de las materias primas y alimentos, en adecuadas condiciones y son reemplazados cada vez que se requiera o se evidencie su deterioro o desgaste, se evidencia soporte de solicitud de reemplazo.', 'Insumos e implementos de aseo', 'Preparado en Sitio\r'),
(98, 98, 'Se evidencia diligenciado el formato de registro diario de asistencia por parte del operador.', 'Otros', 'Preparado en Sitio\r'),
(99, 1, 'Se cuenta con un espacio para el almacenamiento transitorio y distribución de la ración industrializada.', 'Edificacion e instalaciones', 'Industrializado\r'),
(100, 2, 'El lugar de consumo de las raciones industrializadas se encuentra ubicado en un lugar alejado de focos de insalubridad, maleza y aguas estancadas.', 'Edificacion e instalaciones', 'Industrializado\r'),
(101, 3, 'Está constituido en la institución educativa el comité de alimentación escolar (CAE). Cuenta con acta de conformación.', 'Edificacion e instalaciones', 'Industrializado\r'),
(102, 4, 'La institución educativa cuenta con acta de reunion bimensual del comité de alimentación escolar (CAE). ', 'Edificacion e instalaciones', 'Industrializado\r'),
(103, 5, 'Los alimentos se encuentran almacenados transitoriamente en contenedores con tapa o alejados del piso', 'Area de Almacenamiento', 'Industrializado\r'),
(104, 6, 'Existen letreros alusivos a la aplicación de BPM, en buen estado y ubicados en las instalaciones del comedor escolar.', 'Area de Almacenamiento', 'Industrializado\r'),
(105, 7, 'Existe identificación de los contenedores con tapa ó en el área de almacenamiento transitorio de los alimentos', 'Area de Almacenamiento', 'Industrializado\r'),
(106, 8, 'El área de almacenamiento transitorio  y distribución cuenta con las condiciones higiénico sanitarias necesarias (sitio ordenado, pisos y paredes limpias, techo en buen estado, sin grietas y presencia de moho).', 'Area de Almacenamiento', 'Industrializado\r'),
(107, 9, 'Para las I.E. que cuenten con área exclusiva de almacenamiento de alimentos, se realiza el control de plagas (fumigación).', 'Area de Almacenamiento', 'Industrializado\r'),
(108, 10, 'Los alimentos de la ración industrializada se encuentran con empaque primario', 'Empaque', 'Industrializado\r'),
(109, 11, 'Se garantiza cumplimiento al rotulado y etiquetado de todos los alimentos suministrados de manera que en los empaques y envases aparezca la siguiente información: nombre del alimento, ingredientes, información nutricional, contenido neto, peso escurrido, nombre y dirección del fabricante, país de origen, identificación del lote, fecha de vencimiento y/o de duración mínima e instrucciones para conservación, instrucciones de uso, y que las materias primas de calidad cumplan con las especificaciones técnicas descritas en la resolución 00335/21, con registro sanitario INVIMA (Resolución 5109 del 2005, 810 del 2021 y 2492 del 2022)', 'Empaque', 'Industrializado\r'),
(110, 12, 'Se da cumplimiento al menú del día', 'Ciclo de minuta', 'Industrializado\r'),
(111, 13, 'Se evidencia publicado ciclo de menú con dimensiones 64cm x 46cm establecidas por la SED, código QR del menú, QR de atención al ciudadano, además se debe evidenciar la publicación del Noti PAE con línea telefónica y correo electrónico de contacto del operador para la atención de las PQRS.', 'Ciclo de minuta', 'Industrializado\r'),
(112, 14, 'Se evidencia la ficha técnica de información del PAE aprobada y publicada en un lugar visible.', 'Ciclo de minuta', 'Industrializado\r'),
(113, 15, 'Se evidencia que se cumple con la modalidad contratada', 'Características de calidad de los alimentos', 'Industrializado\r'),
(114, 16, 'Los alimentos llegan con el peso y volumen por nivel escolar de acuerdo al ciclo de menú aprobado por la SED.', 'Características de calidad de los alimentos', 'Industrializado\r'),
(115, 17, 'Se evidencia formato de remisión de entrega por nivel escolar, con fecha, hora de entrega, debidamente firmado y las cantidades relacionadas en la remisión son acordes a la  focalización designada.', 'Características de calidad de los alimentos', 'Industrializado\r'),
(116, 18, 'Los productos  (lácteo, cereal, fruta, dulce) cumplen con las características organolépticas y físicas requeridas.', 'Características de calidad de los alimentos', 'Industrializado\r'),
(117, 19, 'Los productos industrializados son los aprobados por el Eje de Calidad e Inocuidad y Alimentación Saludable.', 'Características de calidad de los alimentos', 'Industrializado\r'),
(118, 20, 'Se evidencian que las frutas y empaques de producto lácteo se encuentran lavadas y desinfectadas. ', 'Características de calidad de los alimentos', 'Industrializado\r'),
(119, 21, 'En la minuta industrializada el operador suministra leche entera, leche saborizada y avena  Ultra Alta Temperatura.', 'Características de calidad de los alimentos', 'Industrializado\r'),
(120, 23, 'Las devoluciones realizadas al Operador por causa de baja calidad, deterioro o daño físico, lotes, fecha de producción y vencimiento, son resueltas de manera inmediata.', 'Características de calidad de los alimentos', 'Industrializado\r'),
(121, 24, 'Se evidencia formato de reposición ó entrega de faltante de acuerdo a formato establecido.', 'Características de calidad de los alimentos', 'Industrializado\r'),
(122, 25, 'Se evidencia la  reposición ó entrega de faltante según sea el caso (reposición o faltante) y el diligenciamiento del formato. ', 'Características de calidad de los alimentos', 'Industrializado\r'),
(123, 26, 'Se evidencia que se cumple con los horarios de consumo de los alimentos (Los cambios de horarios deben ser aprobados previamente por el CAE y debe constar acta firmada). ', 'Horario del consumo de alimentos', 'Industrializado\r'),
(124, 27, 'El horario de consumo de los alimentos se encuentra publicado en un lugar visible del comedor escolar', 'Horario del consumo de alimentos', 'Industrializado\r'),
(125, 28, 'El transporte garantiza el mantenimiento de las condiciones de conservación requeridas por el producto alimentario: refrigeración, congelación, recipientes o canastillas de material sanitario con tapa, etc., y cumple con la normatividad vigente. (Resolución 2505 de 2004), no se transportan conjuntamente en un mismo vehículo alimentos o materias primas con sustancias peligrosas y otras sustancias que por su naturaleza representen riesgo de contaminación del alimento o la materia prima (incluye productos de aseo y pipas de gas)', 'Transporte de alimentos', 'Industrializado\r'),
(126, 29, 'El vehículo tiene concepto sanitario favorable, y formulario de inscripción sanitaria para vehículos transportadores de alimentos y bebidas; cuenta con la leyenda \"TRANSPORTE DE ALIMENTOS\".', 'Transporte de alimentos', 'Industrializado\r'),
(127, 30, 'El transportador (conductor y ayudante) cuenta con registro de capacitación continua en aspectos de BPM  según anexo 24, examen medico-ocupacional, vestimenta limpia y adecuada (elementos de protección personal), de acuerdo a la normatividad vigente.', 'Transporte de alimentos', 'Industrializado\r'),
(128, 31, 'Las materias primas son transportadas en canastillas plásticas limpias. el transportador deja copia del registro del previo lavado y desinfección de las mismas desde la bodega hasta las IEO.', 'Transporte de alimentos', 'Industrializado\r'),
(129, 32, 'Los vehículos se encuentran en adecuadas condiciones sanitarias, de aseo y operación para el transporte de los alimentos.', 'Transporte de alimentos', 'Industrializado\r'),
(130, 33, 'El transporte de alimentos cuenta con aviso del Programa de Alimentación Escolar (PAE).', 'Transporte de alimentos', 'Industrializado\r'),
(131, 34, 'El personal manipulador  cuenta con el  uniforme completo (pantalón blanco, camisa o bata blancos y zapatos antideslizantes cerrados blancos) y usan elementos de protección personal (gorro, tapa bocas y guantes en caso de ser necesario).', 'Personal manipulador de alimentos', 'Industrializado\r'),
(132, 35, 'El personal manipulador cuenta con la documentación requerida: certificados médicos, cronograma de capacitaciones (mínimo 10 horas), copia de la entrega de dotación. Debidamente organizada y archivada en la unidad de servicio. ', 'Personal manipulador de alimentos', 'Industrializado\r'),
(133, 36, 'Se evidencia registro de capacitación continua en aspectos de BPM (higiene personal y locativa) y el personal manipulador de alimentos o persona designada posee conocimientos en el tema.', 'Personal manipulador de alimentos', 'Industrializado\r'),
(134, 37, 'Se lleva Registro de Limpieza y desinfección diligenciado de acuerdo al Plan de Saneamiento.', 'Personal manipulador de alimentos', 'Industrializado\r'),
(135, 38, 'Se cuenta con recipientes para la disposición de residuos sólidos apropiados con tapa y son removidos con frecuencia. \nNota: Según Resolución 2148 de 2019. Bolsa  blanca para residuos aprovechables (plástico, cartón vidrio, papel, metales),  bolsa verde para residuos orgánicos aprovechables (restos de comida y desechos agrícolas) y bolsa negra para los residuos no aprovechables (servilletas, papeles y cartones contaminados con comida y papeles metalizados)', 'Insumos e implementos de aseo', 'Industrializado\r'),
(136, 39, 'Se evidencia que los implementos de limpieza y desinfección (desinfectante liquido, jabón de aseo general inoloro, bolsas plásticas de color blanco, verde y negro,  escoba, trapero y  recogedor) según corresponda en la unidades de servicio especificados en la resolución 00335 del 23 de diciembre del 2021', 'Insumos e implementos de aseo', 'Industrializado\r'),
(137, 40, 'Los implementos de aseo  permanecen almacenados en lugares separados de las materias primas y alimentos, en adecuadas condiciones y son reemplazados cada vez que se requiera o se evidencie su deterioro o desgaste, se evidencia soporte de solicitud de reemplazo.', 'Insumos e implementos de aseo', 'Industrializado\r'),
(138, 41, 'Se evidencia diligenciado el formato de registro diario de asistencia por parte del operador.', 'Otros', 'Industrializado\r'),
(139, 1, 'La unidad de servicio esta ubicada en un lugar alejado de focos de insalubridad, maleza y aguas estancadas.', 'Edificacion e instalaciones', 'Jornada Unica\r'),
(140, 2, 'Los techos, paredes y pisos se encuentran en buen estado.', 'Edificacion e instalaciones', 'Jornada Unica\r'),
(141, 3, 'Las puertas se encuentran protegidas para evitar  el ingreso  y refugio de plagas, las aberturas entre las puertas exteriores y los pisos no deben ser mayores a 1 cm. ', 'Edificacion e instalaciones', 'Jornada Unica\r'),
(142, 4, 'Los mesones empleados en el manejo y preparacion de alimentos se encuentran en buen estado.', 'Edificacion e instalaciones', 'Jornada Unica\r'),
(143, 5, 'Las lamparas o bombillos se encuentran protegidas y funcionando. ', 'Edificacion e instalaciones', 'Jornada Unica\r'),
(144, 6, 'No se evidencian instalaciones electricas expuestas en la zona de preparacion', 'Edificacion e instalaciones', 'Jornada Unica\r'),
(145, 7, 'Los sifones y drenajes se encuentran en buen estado, protegidos (rejilla anticucarachas), funcionando y limpios.', 'Edificacion e instalaciones', 'Jornada Unica\r'),
(146, 8, 'Las ventanas y aberturas que se comuniquen con el ambiente exterior estan provistas con malla anti-insecto resistentes, de facil limpieza y bien conservadas.', 'Edificacion e instalaciones', 'Jornada Unica\r'),
(147, 9, 'La institucion educativa cuenta con comedor  para el consumo de los alimentos.', 'Edificacion e instalaciones', 'Jornada Unica\r'),
(148, 10, 'El comedor escolar o espacio destinado cuenta con las mesas y sillas de acuerdo al turno atendido y se encuentran en buen estado.', 'Edificacion e instalaciones', 'Jornada Unica\r'),
(149, 11, 'Se cuenta con un area de almacenamiento protegida e iluminada, con ventilacion natural o artificial.', 'Edificacion e instalaciones', 'Jornada Unica\r'),
(150, 12, 'El area de almacenamiento de las materias primas es acorde a la capacidad de los cupos atendidos.', 'Edificacion e instalaciones', 'Jornada Unica\r'),
(151, 13, 'Esta constituido en la  institucion educativa el comite de alimentacion escolar (CAE). Cuenta con acta de conformacion.', 'Edificacion e instalaciones', 'Jornada Unica\r'),
(152, 14, 'La institucion educativa cuenta con acta de reunion bimensual del comite de alimentacion escolar (CAE). ', 'Edificacion e instalaciones', 'Jornada Unica\r'),
(153, 15, 'La institucion educativa cuenta con servicio de gas propano (dos cilindros 1 de 100lb y 1 de 40lb uno en uso y el otro en reserva cargado) ', 'Area de Almacenamiento', 'Jornada Unica\r'),
(154, 16, 'Los productos o materias primas se encuentran adecuadamente almacenados e identificados y en caso de tener jornada unica esten almacenados de acuerdo a la modalidad. ', 'Area de Almacenamiento', 'Jornada Unica\r'),
(155, 17, 'Se evidencian alimentos libres de algun tipo de contaminacion.', 'Area de Almacenamiento', 'Jornada Unica\r'),
(156, 18, 'Se lleva un control de contramuestras de productos de alto riesgo para la salud (solo aplica para los dos sedes educativas designadas por cada operador)', 'Area de Almacenamiento', 'Jornada Unica\r'),
(157, 19, 'El area de almacenamiento se mantiene limpia y ordenada.', 'Area de Almacenamiento', 'Jornada Unica\r'),
(158, 20, 'Se lleva un control de primeras entradas y primeras salidas con el fin de garantizar la rotacion de los productos.', 'Area de Almacenamiento', 'Jornada Unica\r'),
(159, 21, 'Existe recipientes de almacenamiento de agua adecuados y protegidos con tapa, con la capacidad suficiente para atender como minimo las necesidades correspondientes a un dia de preparacion, si usan recipientes cuentan con registro de limpieza y desinfeccion diligenciado.', 'Area de Almacenamiento', 'Jornada Unica\r'),
(160, 22, 'Se evidencia registro semanal de prueba de calidad del agua, con el kit basico test de PH y cloro residual en las sedes educativas oficiales', 'Area de Almacenamiento', 'Jornada Unica\r'),
(161, 23, 'Se cuenta con recipientes para la disposicion de residuos solidos apropiados con tapa y son removidos con frecuencia. \nNota: Segun  Resolucion 2148 de 2019. Bolsa  blanca para residuos aprovechables (plastico, carton vidrio, papel, metales),  bolsa verde para residuos organicos aprovechables (restos de comida y desechos agricolas) y bolsa negra para los residuos no aprovechables (servilletas, papeles y cartones contaminados con comida y papeles metalizados)', 'Requisitos higienicos ', 'Jornada Unica\r'),
(162, 24, 'La preparacion de los alimentos se realiza cumpliendo con lo estipulado en el plan de saneamiento (limpieza y desinfeccion, manejo de residuos, abastecimiento de agua y manejo integral de plagas).', 'Requisitos higienicos ', 'Jornada Unica\r'),
(163, 25, 'Los pisos, paredes, techos, mesones de las areas de preparacion, distribucion y consumo se encuentran limpios para garantizar condiciones higienico-sanitarias.', 'Requisitos higienicos ', 'Jornada Unica\r'),
(164, 26, 'Todo equipo y utensilio que haya entrado en contacto con materias primas o con material contaminado se limpia y desinfecta cuidadosamente antes de ser nuevamente utilizado.', 'Requisitos higienicos ', 'Jornada Unica\r'),
(165, 27, 'Existen letreros alusivos a la aplicacion de BPM, en buen estado y ubicados en las instalaciones del comedor escolar.', 'Requisitos higienicos ', 'Jornada Unica\r'),
(166, 28, 'Se evidencia en el comedor escolar la implementacion de una ruta de evacuacion caracterizada a la unidad de servicio de los desechos solidos y liquidos.', 'Requisitos higienicos ', 'Jornada Unica\r'),
(167, 29, 'Se dispone de recipiente identificado para la recoleccion de aceite de cocina usado con area destinada para tal fin y se llevan el formato para su contabilizacion', 'Requisitos higienicos ', 'Jornada Unica\r'),
(168, 30, 'Se evidencian que las diferentes areas que conforman el comedor escolar estan  identificadas y señalizadas con avisos elaborados en material lavable, resistente y se encuentran en buen estado.', 'Requisitos higienicos ', 'Jornada Unica\r'),
(169, 31, 'La Institucion Educativa cuenta con concepto higienico sanitario favorable o favorable con requerimientos o solicitud de visita por parte del operador para realizar visita por secretaria de salud.', 'Requisitos higienicos ', 'Jornada Unica\r'),
(170, 32, 'Los productos se encuentran con fecha de vencimiento vigente y son aptos para el consumo.', 'Caracteristicas de calidad de los alimentos.', 'Jornada Unica\r'),
(171, 33, 'Los productos utilizados en la unidad de servicio para la preparacion son avalados por el Eje de Calidad e Inocuidad y Alimentacion Saludable', 'Caracteristicas de calidad de los alimentos.', 'Jornada Unica\r'),
(172, 34, 'Se lleva registro de temperatura de los alimentos preparados en sitio : \ncontrol de temperatura 2 veces durante el tratamiento termico de la preparacion (minimo 75º C) y al inicio de la distribucion a los titulares de derecho (Minimo 65 ºC).', 'Caracteristicas de calidad de los alimentos', 'Jornada Unica\r'),
(173, 35, 'Se evidencia que el alimento a servir se encuentra a temperatura igual o mayor a 65°C.', 'Caracteristicas de calidad de los alimentos', 'Jornada Unica\r'),
(174, 36, 'Se evidencia formato de remision de entrega por nivel escolar, con fecha, hora de entrega, debidamente firmado y las cantidades relacionadas en la remision son acordes a la focalizacion designada.', 'Caracteristicas de calidad de los alimentos', 'Jornada Unica\r'),
(175, 37, 'Se evidencia entrega de la racion alimentaria designada al personal manipulador de alimentos.', 'Caracteristicas de calidad de los alimentos', 'Jornada Unica\r'),
(176, 38, 'El inventario de los productos o materia prima estan acorde a los cupos focalizados y nivel escolar.', 'Caracteristicas de calidad de los alimentos', 'Jornada Unica\r'),
(177, 39, 'Se garantiza cumplimiento al rotulado y etiquetado de todos los alimentos suministrados de manera que en los empaques y envases aparezca la siguiente informacion: nombre del alimento, ingredientes, informacion nutricional, contenido neto, peso escurrido, nombre y direccion del fabricante, pais de origen, identificacion del lote, fecha de vencimiento y/o de duracion minima e instrucciones para conservacion, instrucciones de uso, y que las materias primas de calidad cumplan con las especificaciones tecnicas descritas en la resolucion 00335/21, con registro sanitario INVIMA (Resolucion 5109 del 2005, 810 del 2021, 2492 del 2022)', 'Caracteristicas de calidad de los alimentos', 'Jornada Unica\r'),
(178, 40, 'Los productos cumplen con las caracteristicas organolepticas y fisicas requeridas, En caso de suministrarse fruta porcionada, la cual por su composicion quimica presente reacciones de pardeamiento enzimatico (banano, manzana, pera), el operador debera garantizar procedimientos no quimicos para evitar esta alteracion en sus caracteristicas organolepticas.', 'Caracteristicas de calidad de los alimentos', 'Jornada Unica\r'),
(179, 41, 'Los alimentos altamente perecederos (proteina, lacteos o alimentos de alto riesgo) se encuentran almacenados y refrigerados a temperatura que garantice su conservacion (entre 0 a 4° C) en refrigeracion y (temperaturas inferior a 0°C) en congelacion, y se evidencia registro de temperatura minimo una vez al dia', 'Caracteristicas de calidad de los alimentos', 'Jornada Unica\r'),
(180, 42, 'Se evidencian las guias de preparacion en la unidad de servicio y se encuentran ajustadas al ciclo de menu.', 'Caracteristicas de calidad de los alimentos', 'Jornada Unica\r'),
(181, 43, 'Los alimentos son preparados acorde con las guias de preparacion estipuladas', 'Caracteristicas de calidad de los alimentos', 'Jornada Unica\r'),
(182, 44, 'Los cortes de carne empleados para la preparacion de los menu son acordes a lo establecido por la SED  (Res (caderita, centro de pierna, bola negra) cerdo (brazo y pierna) y pollo (filete de pechuga de pollo sin marinar / pechuga sin piel, sin hueso y sin marinar/ pechuga con piel y hueso sin marinar por beneficiario se debera calcular con base al 65% de parte comestible).', 'Caracteristicas de calidad de los alimentos', 'Jornada Unica\r'),
(183, 45, 'Las reposiciones realizadas al operador por causa de baja calidad, deterioro o daño fisico, lotes, fecha de produccion y vencimiento, son resueltas de manera inmediata.', 'Caracteristicas de calidad de los alimentos', 'Jornada Unica\r'),
(184, 46, 'Se evidencia formato de reposicion o entrega de faltante de acuerdo a formato establecido por la SED', 'Caracteristicas de calidad de los alimentos', 'Jornada Unica\r'),
(185, 47, 'Se evidencia la reposicion o entrega de faltante segun sea el caso (reposicion o faltante) y el diligenciamiento del formato. ', 'Caracteristicas de calidad de los alimentos', 'Jornada Unica\r'),
(186, 48, 'Para las I.E  se evidencia  registro de control de temperatura en la recepcion de los alimentos altamente perecederos (res, cerdo y pollo).\n', 'Caracteristicas de calidad de los alimentos', 'Jornada Unica\r'),
(187, 49, 'El operador garantiza la inocuidad de los alimentos, evitando la contaminacion cruzada en las diferentes etapas (Almacenamiento, Preparacion y distribucion)', 'Caracteristicas de calidad de los alimentos', 'Jornada Unica\r'),
(188, 50, 'La unidad de servicio cuenta con la cantidad de manipuladora(e)s necesarios de acuerdo al numero de raciones o de acuerdo a lo aprobado por la SED\n', 'Personal manipulador de alimentos', 'Jornada Unica\r'),
(189, 51, 'La presentacion personal de los manipuladores es adecuada (uñas cortas, limpias y sin esmalte, cabello recogido, sin uso de joyas u otros accesorios ni maquillaje).', 'Personal manipulador de alimentos', 'Jornada Unica\r'),
(190, 52, 'El personal manipulador cuenta con la documentacion requerida: certificados medicos, cronograma de capacitaciones (minimo 10 horas), copia de la entrega de dotacion. Debidamente organizada y archivada en la unidad de servicio.', 'Personal manipulador de alimentos', 'Jornada Unica\r'),
(191, 53, 'Se evidencia registro de capacitacion en Salud Ocupacional y el personal manipulador de alimentos tiene conocimiento del tema', 'Personal manipulador de alimentos', 'Jornada Unica\r'),
(192, 54, 'Se evidencia registro de capacitacion continua en aspectos de BPM (higiene personal y locativa) y el personal manipulador de alimentos posee conocimientos en el tema', 'Personal manipulador de alimentos', 'Jornada Unica\r'),
(193, 55, 'Se evidencia registro de capacitacion en preparacion de alimentos y el personal manipulador de alimentos demuestra conocimiento del tema', 'Personal manipulador de alimentos', 'Jornada Unica\r'),
(194, 56, 'El personal manipulador cuenta con certificado de capacitacion en manipulacion de alimentos o plan de capacitacion y listado de asistencia.', 'Personal manipulador de alimentos', 'Jornada Unica\r'),
(195, 57, 'Se evidencia registro de capacitacion en minuta patron, ciclo de menu y conoce del tema', 'Personal manipulador de alimentos', 'Jornada Unica\r'),
(196, 58, 'Se evidencia registro de capacitacion en manejo y diligenciamiento de formatos (plan de saneamiento, entradas y salidas, formato de faltantes, formatos de registro de temperaturas)', 'Personal manipulador de alimentos', 'Jornada Unica\r'),
(197, 59, 'Se evidencia registro de capacitacion en estandarizacion de porciones y servido de alimentos.', 'Personal manipulador de alimentos', 'Jornada Unica\r'),
(198, 60, 'Se evidencia registro de capacitacion en plan de saneamiento y conoce del tema', 'Personal manipulador de alimentos', 'Jornada Unica\r'),
(199, 61, 'El personal manipulador cuenta con el uniforme completo (pantalon blanco, camisa o bata blancos, zapatos antideslizantes cerrados blancos y delantal plastico) y usan elementos de proteccion personal (gorro, tapa bocas y guantes en caso de ser necesario).', 'Personal manipulador de alimentos', 'Jornada Unica\r'),
(200, 62, 'Se exige al personal externo que visite las areas de almacenamiento, preparacion y/o participe en la distribucion de alimentos de los comedores escolares, el uso de la dotacion y el cumplimiento de las practicas de higiene y de manipulacion de alimentos establecidas en la normatividad sanitaria vigente. ', 'Personal manipulador de alimentos', 'Jornada Unica\r'),
(201, 63, 'Se evidencia que se cumple con la modalidad contratada', 'Ciclo de minuta', 'Jornada Unica\r'),
(202, 64, 'Se evidencia publicado ciclo de menu con dimensiones 64cm x 46cm establecidas por la SED, QR de atencion al ciudadano, ademas se debe evidenciar la publicacion del Noti PAE con linea telefonica y correo electronico de contacto del operador para la atencion de las PQRS.', 'Ciclo de minuta', 'Jornada Unica\r'),
(203, 65, 'Se da cumplimiento al menu del dia', 'Ciclo de minuta', 'Jornada Unica\r'),
(204, 66, 'Se cumple con el peso servido de acuerdo al ciclo de menu por nivel escolar.', 'Ciclo de minuta', 'Jornada Unica\r'),
(205, 67, 'Se evidencia la lista de intercambios en el comedor escolar', 'Ciclo de minuta', 'Jornada Unica\r'),
(206, 68, 'Se evidencia la ficha tecnica de informacion del PAE aprobado y publicado en un lugar visible.', 'Ciclo de minuta', 'Jornada Unica\r'),
(207, 69, 'Se evidencia el cumplimiento del manual de imagen en la documentacion (formatos, avisos, informes, procedimientos e instructivos) ', 'Ciclo de minuta', 'Jornada Unica\r'),
(208, 70, 'El horario de consumo de los alimentos se encuentra publicado en un lugar visible del comedor escolar', 'Horario del consumo de alimentos', 'Jornada Unica\r'),
(209, 71, 'Se evidencia que se cumple con los horarios de consumo de los alimentos (Los cambios de horarios deben ser aprobados previamente por el CAE y debe constar acta firmada). ', 'Horario del consumo de alimentos', 'Jornada Unica\r'),
(210, 72, 'Se evidencia Plan de Saneamiento en tamaño adecuado de letra, acorde a  la Unidad de Servicio, cumpliendo con los programas: limpieza y desinfeccion, control de plagas, desechos solidos y abastecimiento o suministro de agua.', 'Plan de Saneamiento', 'Jornada Unica\r'),
(211, 73, 'Se lleva Registro de Limpieza y desinfeccion diligenciado de acuerdo al Plan de Saneamiento.', 'Plan de Saneamiento', 'Jornada Unica\r'),
(212, 74, 'Se garantiza que los equipos para el almacenameinto de los alimentos y utensilios se encuentran en adecuadas condiciones de limpieza y desinfeccion.', 'Plan de Saneamiento', 'Jornada Unica\r'),
(213, 75, 'Se evidencia certificado de control de plagas en la unidad de servicio vigente.', 'Plan de Saneamiento', 'Jornada Unica\r'),
(214, 76, 'Se observa registros de las actividades realizadas y tipo de sustancias empleadas ', 'Plan de Saneamiento', 'Jornada Unica\r'),
(215, 77, 'Se evidencia el formato para el registro semanal de las actividades para control de plagas debidamente diligenciado. ', 'Plan de Saneamiento', 'Jornada Unica\r'),
(216, 78, 'Se evidencia cronograma para el control de plagas en el comedor escolar (fumigacion, desratizacion y desinsectacion) y se cumple con el mismo.', 'Plan de Saneamiento', 'Jornada Unica\r'),
(217, 79, 'Las instalaciones y/o alimentos se encuentran libres de daños causados por plagas o roedores (ratas, hormigas, palomas, cucarachas, etc.).', 'Plan de Saneamiento', 'Jornada Unica\r'),
(218, 80, 'Se garantiza el adecuado almacenamiento de los elementos y sustancias de limpieza y desinfeccion en contenedores y las areas establecidas con hoja o carta de seguridad, debidamente identificadas evitando el contacto con las materias primas, alimentos preparados, utensilios y menaje.', 'Plan de Saneamiento', 'Jornada Unica\r'),
(219, 81, 'Se evidencia que las materias primas crudas tales como  verduras, hortalizas, frutas y huevos se lavan y/o desinfectan antes de su preparacion.', 'Plan de Saneamiento', 'Jornada Unica\r');
INSERT INTO `preguntas_tecnica` (`id_tecnica`, `numero`, `preguntas`, `categorias`, `tipo_racion`) VALUES
(220, 82, 'El transporte garantiza el mantenimiento de las condiciones de conservacion requeridas por el producto alimentario: refrigeracion, congelacion, recipientes o canastillas de material sanitario con tapa, etc., y cumple con la normatividad vigente. (Resolucion 2505 de 2004), no se transportan conjuntamente en un mismo vehiculo alimentos o materias primas con sustancias peligrosas y otras sustancias que por su naturaleza representen riesgo de contaminacion del alimento o la materia prima (incluye productos de aseo y pipas de gas)', 'Transporte de alimentos', 'Jornada Unica\r'),
(221, 83, 'Las materias primas son transportadas en canastillas plasticas limpias. el transportador deja copia del registro del previo lavado y desinfecion de las mismas desde la bodega hasta las Institucion Educativa Oficial.', 'Transporte de alimentos', 'Jornada Unica\r'),
(222, 84, 'Los vehiculos se encuentran en adecuadas condiciones sanitarias, de aseo y operacion para el transporte de los alimentos.', 'Transporte de alimentos', 'Jornada Unica\r'),
(223, 85, 'El vehiculo tiene concepto sanitario favorable, formato de limpieza y desinfeccion del vehiculo y formulario de inscripcion sanitaria para vehiculos transportadores de alimentos y bebidas.', 'Transporte de alimentos', 'Jornada Unica\r'),
(224, 86, 'El transporte de alimentos cuenta con aviso del Programa de Alimentacion Escolar (PAE).', 'Transporte de alimentos', 'Jornada Unica\r'),
(225, 87, 'El transportador (conductor y ayudante) cuenta con registro de capacitacion continua en aspectos de BPM  segun anexo 24, examen medico-ocupacional, vestimenta limpia y adecuada (elementos de proteccion personal), de acuerdo a la normatividad vigente.', 'Transporte de alimentos', 'Jornada Unica\r'),
(226, 88, 'El personal manipulador puede verificar la cantidad de materia prima recepcionada, ya sea con bascula en la IOE o vehiculo.', 'Transporte de alimentos', 'Jornada Unica\r'),
(227, 89, 'Los equipos (estufa, licuadora, equipo de frio),  utilizados en la preparacion se encuentran funcionando adecuadamente y cuentan con hoja de vida.', 'Equipo y utensilios ', 'Jornada Unica\r'),
(228, 90, 'Los equipos de medicion (gramera, termometro y balanza) cuentan con registro de verificacion de masa y temperatura.', 'Equipo y utensilios ', 'Jornada Unica\r'),
(229, 91, 'Las neveras, congeladores y demas equipos de almacenamiento cuentan con registro de temperatura (minimo una vez al dia)', 'Equipo y utensilios ', 'Jornada Unica\r'),
(230, 92, 'Los utensilios tales como tablas, cucharas, ollas y demas menaje estan fabricados con materiales sanitarios, resistentes a la corrosion de facil limpieza y desinfeccion y se encuentran en buen estado.', 'Equipo y utensilios ', 'Jornada Unica\r'),
(231, 93, 'Se cuenta con los equipos y utensilios minimos requeridos para la prestacion del servicio segun modalidad ', 'Equipo y utensilios ', 'Jornada Unica\r'),
(232, 94, 'El operador garantiza como minimo el 60% del menaje (platos, vasos, cucharas) y equipos  (nevera, estufa, licuadora y congelador) correspondientes a lo focalizado en la IEO  y se evidencia la relacion en la carpeta tecnica.', 'Equipo y utensilios ', 'Jornada Unica\r'),
(233, 95, 'Se evidencia dotacion de los elementos de higiene personal (jabon liquido antibacterial inoloro, papel higienico).', 'Insumos e implementos de aseo', 'Jornada Unica\r'),
(234, 96, 'Se evidencia que los implementos de limpieza y desinfeccion (desinfectante liquido, detergente biodegradable para el lavado de platos inoloro, esponja de fibra abrasiva media, limpiones en microfibra, toallas absorbentes, jabon de aseo general inoloro, bolsas plasticas de color blanco, verde y negro, esponja plastica para el lavado de ollas, escoba, trapero y  recogedor) se encuentran en la cantidad requerida de acuerdo al cupo atendido  para complemento alimentario y jornada unica, segun corresponda en la unidades de servicio especificados en la resolucion 335 del 23 de diciembre del 2021.', 'Insumos e implementos de aseo', 'Jornada Unica\r'),
(235, 97, 'Los implementos de aseo  permanecen almacenados en lugares separados de las materias primas y alimentos, en adecuadas condiciones y son reemplazados cada vez que se requiera o se evidencie su deterioro o desgaste, se evidencia soporte de solicitud de reemplazo.', 'Insumos e implementos de aseo', 'Jornada Unica\r'),
(236, 98, 'Se evidencia diligenciado el formato de registro diario de asistencia por parte del operador.', 'Otros', 'Jornada Unica\r');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `preparadoensitioam`
--

CREATE TABLE `preparadoensitioam` (
  `id_preparado_sitio_am` int(11) NOT NULL,
  `semana` int(11) NOT NULL,
  `numero_menu` int(11) NOT NULL,
  `id_tipo_racion` int(11) NOT NULL,
  `componentes` text NOT NULL,
  `ingredientes` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `preparadoensitioam`
--

INSERT INTO `preparadoensitioam` (`id_preparado_sitio_am`, `semana`, `numero_menu`, `id_tipo_racion`, `componentes`, `ingredientes`) VALUES
(1, 1, 1, 2, 'LACTEOS', 'CHOCOLATE CON LECHE\r'),
(2, 1, 1, 2, 'ALIMENTO PROTEICO', 'HUEVOS REVUELTOS\r'),
(3, 1, 1, 2, 'DERIVADO CEREAL', 'ARROZ BLANCO PAN\r'),
(4, 1, 1, 2, 'FRUTA', 'N/A\r'),
(5, 1, 2, 2, 'LACTEOS', 'AGUA DE PANELA CON LECHE\r'),
(6, 1, 2, 2, 'ALIMENTO PROTEICO', 'SANDWICH DE QUESO\n'),
(7, 1, 2, 2, 'DERIVADO CEREAL', 'PAN EN SANDWICH PAPAS A LA FRANCESA\r'),
(8, 1, 2, 2, 'FRUTA', 'SANDIA\r'),
(9, 1, 3, 2, 'LACTEOS', 'ARROZ CON LECHE Y CANELA MOLIDA\r'),
(10, 1, 3, 2, 'ALIMENTO PROTEICO', 'N/A\r'),
(11, 1, 3, 2, 'DERIVADO CEREAL', 'ARROZ EN LA BEBIDA LACTEA PALITO DE HARINA DE TRIGO\n'),
(12, 1, 3, 2, 'FRUTA', 'MANZANA\r'),
(13, 1, 4, 2, 'LACTEOS', 'CHOCOLATE CON LECHE\r'),
(14, 1, 4, 2, 'ALIMENTO PROTEICO', 'PECHUGA POLLO EN TROZOS GUISADO CON PAPA\r'),
(15, 1, 4, 2, 'DERIVADO CEREAL', 'AREPA ASADA ARROZ BLANCO\r'),
(16, 1, 4, 2, 'FRUTA', 'N/A\r'),
(17, 1, 5, 2, 'LACTEOS', 'COLADA DE AVENA CON LECHE\r'),
(18, 1, 5, 2, 'ALIMENTO PROTEICO', 'HUEVOS REVUELTOS\r'),
(19, 1, 5, 2, 'DERIVADO CEREAL', 'MASITAS DE HARINA DE TRIGO\r'),
(20, 1, 5, 2, 'FRUTA', 'MIX DE MANGO Y PINA EN TROZOS\r'),
(21, 2, 6, 2, 'LACTEOS', 'REFRESCO DE AVENA CON LECHE\r'),
(22, 2, 6, 2, 'ALIMENTO PROTEICO', 'HUEVOS PERICOS CON ESPINACA\r'),
(23, 2, 6, 2, 'DERIVADO CEREAL', 'ARROZ BLANCO PLATANO COCIDO\n'),
(24, 2, 6, 2, 'FRUTA', 'N/A\r'),
(25, 2, 7, 2, 'LACTEOS', 'CHOCOLATE CON LECHE\r'),
(26, 2, 7, 2, 'ALIMENTO PROTEICO', 'CARNE DE RES EN TROZOS CON GUISO\r'),
(27, 2, 7, 2, 'DERIVADO CEREAL', 'ARROZ BLANCO PAN\r'),
(28, 2, 7, 2, 'FRUTA', 'GRANADILLA\r'),
(29, 2, 8, 2, 'LACTEOS', 'COLADA DE AVENA CON LECHE\r'),
(30, 2, 8, 2, 'ALIMENTO PROTEICO', 'HUEVOS REVUELTOS\r'),
(31, 2, 8, 2, 'DERIVADO CEREAL', 'MASITAS DE HARINA DE TRIGO\r'),
(32, 2, 8, 2, 'FRUTA', 'MANDARINA\r'),
(33, 2, 9, 2, 'LACTEOS', 'CHOCOLATE CON LECHE\r'),
(34, 2, 9, 2, 'ALIMENTO PROTEICO', 'QUESO CUAJADA\r'),
(35, 2, 9, 2, 'DERIVADO CEREAL', 'PAN ALINADO\r'),
(36, 2, 9, 2, 'FRUTA', 'MIX DE MANGO Y PAPAYA\r'),
(37, 2, 10, 2, 'LACTEOS', 'AGUA DE PANELA CON LECHE\r'),
(38, 2, 10, 2, 'ALIMENTO PROTEICO', 'SANDWICH DE POLLO\n'),
(39, 2, 10, 2, 'DERIVADO CEREAL', 'PAN EN SANDWICH MONEDITAS DE PLATANO\n'),
(40, 2, 10, 2, 'FRUTA', 'N/A\r'),
(41, 3, 11, 2, 'LACTEOS', 'CHOCOLATE CON LECHE\r'),
(42, 3, 11, 2, 'ALIMENTO PROTEICO', 'HUEVOS REVUELTOS CON PAPA\r'),
(43, 3, 11, 2, 'DERIVADO CEREAL', 'ARROZ CON FIDEOS\r'),
(44, 3, 11, 2, 'FRUTA', 'N/A\r'),
(45, 3, 12, 2, 'LACTEOS', 'AGUA DE PANELA CON LECHE\r'),
(46, 3, 12, 2, 'ALIMENTO PROTEICO', 'SANDWICH DE CERDO\r'),
(47, 3, 12, 2, 'DERIVADO CEREAL', 'PAN EN EL SANDWICH MONEDITAS DEL PLATANO\n'),
(48, 3, 12, 2, 'FRUTA', 'N/A\r'),
(49, 3, 13, 2, 'LACTEOS', 'CHOCOLATE CON LECHE\r'),
(50, 3, 13, 2, 'ALIMENTO PROTEICO', 'QUESO CUAJADA\r'),
(51, 3, 13, 2, 'DERIVADO CEREAL', 'AREPA ASADA\r'),
(52, 3, 13, 2, 'FRUTA', 'MANGO PICADO\r'),
(53, 3, 14, 2, 'LACTEOS', 'AGUA DE PANELA CON LECHE\r'),
(54, 3, 14, 2, 'ALIMENTO PROTEICO', 'FAJITAS DE POLLO ASADO\r'),
(55, 3, 14, 2, 'DERIVADO CEREAL', 'PAPA ABORRAJADA ARROZ BLANCO\r'),
(56, 3, 14, 2, 'FRUTA', 'PINA PICADA\r'),
(57, 3, 15, 2, 'LACTEOS', 'ARROZ CON LECHE Y CANELA MOLIDA\r'),
(58, 3, 15, 2, 'ALIMENTO PROTEICO', 'N/A\r'),
(59, 3, 15, 2, 'DERIVADO CEREAL', 'ARROZ EN LA BEBIDA LACTEA GALLETAS DE SODA CON MARGARINA\r'),
(60, 3, 15, 2, 'FRUTA', 'PERA\r'),
(61, 4, 16, 2, 'LACTEOS', 'CHOCOLATE CON LECHE\r'),
(62, 4, 16, 2, 'ALIMENTO PROTEICO', 'HUEVOS PERICOS\r'),
(63, 4, 16, 2, 'DERIVADO CEREAL', 'AREPA ASADA ARROZ BLANCO\r'),
(64, 4, 16, 2, 'FRUTA', 'N/A\r'),
(65, 4, 17, 2, 'LACTEOS', 'AGUA DE PANELA CON LECHE\r'),
(66, 4, 17, 2, 'ALIMENTO PROTEICO', 'SANDWICH DE PECHUGA DE POLLO\n'),
(67, 4, 17, 2, 'DERIVADO CEREAL', 'PAN EN EL SANDWICH MONEDITAS DE PLATANO\r'),
(68, 4, 17, 2, 'FRUTA', 'PAPAYA PICADA\r'),
(69, 4, 18, 2, 'LACTEOS', 'REFRESCO DE AVENA CON LECHE\r'),
(70, 4, 18, 2, 'ALIMENTO PROTEICO', 'HUEVOS REVUELTOS\r'),
(71, 4, 18, 2, 'DERIVADO CEREAL', 'MASITAS DE HARINA DE TRIGO\r'),
(72, 4, 18, 2, 'FRUTA', 'PINA PICADA'),
(73, 4, 19, 2, 'LACTEOS', 'COLADA DE AVENA CON LECHE\r'),
(74, 4, 19, 2, 'ALIMENTO PROTEICO', 'FAJITAS DE CARNE DE CERDO SALTEADAS\r'),
(75, 4, 19, 2, 'DERIVADO CEREAL', 'PAPA ABORRAJADA CON PICO DE GALLO ARROZ BLANCO\r'),
(76, 4, 19, 2, 'FRUTA', 'MANDARINA\r'),
(77, 4, 20, 2, 'LACTEOS', 'AGUA DE PANELA CON LECHE\r'),
(78, 4, 20, 2, 'ALIMENTO PROTEICO', 'FRIJOLES GUISADOS\r'),
(79, 4, 20, 2, 'DERIVADO CEREAL', 'TAJADAS DE PLATANO FRITO ARROZ BLANCO\n'),
(80, 4, 20, 2, 'FRUTA', 'N/A\r');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `preparadoensitiopm`
--

CREATE TABLE `preparadoensitiopm` (
  `id_preparado_sitio_pm` int(11) NOT NULL,
  `semana` int(11) DEFAULT NULL,
  `numero_menu` int(11) DEFAULT NULL,
  `id_tipo_racion` int(11) DEFAULT NULL,
  `componentes` text DEFAULT NULL,
  `ingredientes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `preparadoensitiopm`
--

INSERT INTO `preparadoensitiopm` (`id_preparado_sitio_pm`, `semana`, `numero_menu`, `id_tipo_racion`, `componentes`, `ingredientes`) VALUES
(1, 1, 1, 3, 'LACTEOS', 'SORBETE DE GUANABANA\r'),
(2, 1, 1, 3, 'ALIMENTO PROTEICO', 'HABICHUELA Y ZANAHORIA CON HUEVO\r'),
(3, 1, 1, 3, 'DERIVADO CEREAL', 'ARROZ BLANCO Y PLATANO COCIDO\n'),
(4, 1, 1, 3, 'FRUTA', 'N/A\r'),
(5, 1, 1, 3, 'ENSALADA VERDURAS', 'N/A\r'),
(6, 1, 2, 3, 'LACTEOS', 'SORBETE DE MARACUYA\n'),
(7, 1, 2, 3, 'ALIMENTO PROTEICO', 'FAJITAS DE POLLO SALTEADO CON VERDURAS (CEBOLLA ZANAHORIA Y ARVEJA)\r'),
(8, 1, 2, 3, 'DERIVADO CEREAL', 'ESPAGUETTIS EN SALSA CRIOLLA Y ARROZ BLANCO\r'),
(9, 1, 2, 3, 'FRUTA', 'MANDARINA\r'),
(10, 1, 2, 3, 'ENSALADA VERDURAS', 'N/A\r'),
(11, 1, 3, 3, 'LACTEOS', 'SORBETE DE FRESA\r'),
(12, 1, 3, 3, 'ALIMENTO PROTEICO', 'HUEVO REVUELTO\r'),
(13, 1, 3, 3, 'DERIVADO CEREAL', 'ARROZ BLANCO CON FRIJOLES GUISADOS Y TAJADAS DE PLATANO FRITO\n'),
(14, 1, 3, 3, 'FRUTA', 'N/A\r'),
(15, 1, 3, 3, 'ENSALADA VERDURAS', 'ENS LECHUGA CON ZANAHORIA RALLADA\r'),
(16, 1, 4, 3, 'LACTEOS', 'SORBETE DE MANGO\r'),
(17, 1, 4, 3, 'ALIMENTO PROTEICO', 'GOULASH DE CERDO CON PAPA HABICHUELA Y ZANAHORIA\r'),
(18, 1, 4, 3, 'DERIVADO CEREAL', 'ARROZ BLANCO\r'),
(19, 1, 4, 3, 'FRUTA', 'SANDIA\n'),
(20, 1, 4, 3, 'ENSALADA VERDURAS', 'N/A\r'),
(21, 1, 5, 3, 'LACTEOS', 'SORBETE DE GUAYABA\r'),
(22, 1, 5, 3, 'ALIMENTO PROTEICO', 'N/A\r'),
(23, 1, 5, 3, 'DERIVADO CEREAL', 'ARROZ BLANCO CON LENTEJAS Y PAPAS A LA FRANCESA\r'),
(24, 1, 5, 3, 'FRUTA', 'MIX DE MANGO Y PAPAYA\r'),
(25, 1, 5, 3, 'ENSALADA VERDURAS', 'RODAJAS DE TOMATE\r'),
(26, 2, 6, 3, 'LACTEOS', 'SORBETE DE MARACUYA\n'),
(27, 2, 6, 3, 'ALIMENTO PROTEICO', 'HUEVOS REVUELTOS\r'),
(28, 2, 6, 3, 'DERIVADO CEREAL', 'ARROZ BLANCO Y TAJADAS DE PLATANO MADURO\n'),
(29, 2, 6, 3, 'FRUTA', 'N/A\r'),
(30, 2, 6, 3, 'ENSALADA VERDURAS', 'ENS LECHUGA CON HABICHUELA\r'),
(31, 2, 7, 3, 'LACTEOS', 'SORBETE DE GUAYABA\r'),
(32, 2, 7, 3, 'ALIMENTO PROTEICO', 'CARNE DE RES SALTEADA CON ZANAHORIA Y ARVEJA\r'),
(33, 2, 7, 3, 'DERIVADO CEREAL', 'ARROZ BLANCO Y PAPA CRIOLLA DORADA\r'),
(34, 2, 7, 3, 'FRUTA', 'BANANO\r'),
(35, 2, 7, 3, 'ENSALADA VERDURAS', 'N/A\r'),
(36, 2, 8, 3, 'LACTEOS', 'SORBETE DE MANGO\r'),
(37, 2, 8, 3, 'ALIMENTO PROTEICO', 'HUEVO PERICO\r'),
(38, 2, 8, 3, 'DERIVADO CEREAL', 'ARROZ BLANCO\r'),
(39, 2, 8, 3, 'FRUTA', 'PAPAYA PICADA\r'),
(40, 2, 8, 3, 'ENSALADA VERDURAS', 'N/A\r'),
(41, 2, 9, 3, 'LACTEOS', 'SORBETE DE GUANABANA\r'),
(42, 2, 9, 3, 'ALIMENTO PROTEICO', 'SANDWICH DE POLLO APANADO\n'),
(43, 2, 9, 3, 'DERIVADO CEREAL', 'PAN EN EL SANDWICH Y PAPAS A LA FRANCESA\n'),
(44, 2, 9, 3, 'FRUTA', 'N/A\r'),
(45, 2, 9, 3, 'ENSALADA VERDURAS', 'LECHUGA Y TOMATE ENTRE EL SANDWICH\n'),
(46, 2, 10, 3, 'LACTEOS', 'REFRESCO DE AVENA\r'),
(47, 2, 10, 3, 'ALIMENTO PROTEICO', 'N/A\r'),
(48, 2, 10, 3, 'DERIVADO CEREAL', 'ARROZ BLANCO CON FRIJOLES GUISADOS Y PLATANO MADURO FRITO\n'),
(49, 2, 10, 3, 'FRUTA', 'MANDARINA\r'),
(50, 2, 10, 3, 'ENSALADA VERDURAS', 'N/A\r'),
(51, 3, 11, 3, 'LACTEOS', 'SORBETE DE MANGO\r'),
(52, 3, 11, 3, 'ALIMENTO PROTEICO', 'HUEVOS REVUELTOS CON PAPA\r'),
(53, 3, 11, 3, 'DERIVADO CEREAL', 'ARROZ CON CILANTRO\r'),
(54, 3, 11, 3, 'FRUTA', 'N/A\r'),
(55, 3, 11, 3, 'ENSALADA VERDURAS', 'ENS ESPINACA Y LECHUGA\r'),
(56, 3, 12, 3, 'LACTEOS', 'SORBETE DE FRESA\r'),
(57, 3, 12, 3, 'ALIMENTO PROTEICO', 'PECHUGA DE POLLO SALTEADA\r'),
(58, 3, 12, 3, 'DERIVADO CEREAL', 'ARROZ CON HABICHUELA Y PAPA GUISADA\r'),
(59, 3, 12, 3, 'FRUTA', 'PINA EN TROZOS\n'),
(60, 3, 12, 3, 'ENSALADA VERDURAS', 'N/A\r'),
(61, 3, 13, 3, 'LACTEOS', 'SORBETE DE MARACUYA\n'),
(62, 3, 13, 3, 'ALIMENTO PROTEICO', 'CARNE DE RES PICADA\r'),
(63, 3, 13, 3, 'DERIVADO CEREAL', 'ARROZ BLANCO CON FRIJOLES GUISADOS Y TAJADAS DE PLATANO FRITO\n'),
(64, 3, 13, 3, 'FRUTA', 'MANGO PICADO\r'),
(65, 3, 13, 3, 'ENSALADA VERDURAS', 'N/A\r'),
(66, 3, 14, 3, 'LACTEOS', 'REFRESCO DE AVENA\r'),
(67, 3, 14, 3, 'ALIMENTO PROTEICO', 'HAMBURGUESA DE CARNE DE CERDO\r'),
(68, 3, 14, 3, 'DERIVADO CEREAL', 'PAN EN LA HAMBURGUESA Y PAPAS A LA FRANCESA\r'),
(69, 3, 14, 3, 'FRUTA', 'N/A\r'),
(70, 3, 14, 3, 'ENSALADA VERDURAS', 'LECHUGA Y TOMATE ENTRE LA HAMBURGUESA\r'),
(71, 3, 15, 3, 'LACTEOS', 'SORBETE DE GUAYABA\r'),
(72, 3, 15, 3, 'ALIMENTO PROTEICO', 'N/A\r'),
(73, 3, 15, 3, 'DERIVADO CEREAL', 'ARROZ BLANCO CON LENTEJAS GUISADAS Y MONEDITAS DE PLATANO\n'),
(74, 3, 15, 3, 'FRUTA', 'PAPAYA PICADA\r'),
(75, 3, 15, 3, 'ENSALADA VERDURAS', 'N/A\r'),
(76, 4, 16, 3, 'LACTEOS', 'SORBETE DE BANANO\r'),
(77, 4, 16, 3, 'ALIMENTO PROTEICO', 'HUEVOS PERICOS\r'),
(78, 4, 16, 3, 'DERIVADO CEREAL', 'ARROZ BLANCO Y PAN\r'),
(79, 4, 16, 3, 'FRUTA', 'N/A\r'),
(80, 4, 16, 3, 'ENSALADA VERDURAS', 'N/A\r'),
(81, 4, 17, 3, 'LACTEOS', 'SORBETE DE GUANABANA\r'),
(82, 4, 17, 3, 'ALIMENTO PROTEICO', 'FAJITAS DE PECHUGA DE POLLO GUISADAS CON HABICHUELA Y ZANAHORIA\r'),
(83, 4, 17, 3, 'DERIVADO CEREAL', 'ARROZ BLANCO\r'),
(84, 4, 17, 3, 'FRUTA', 'PINA EN TROZOS\n'),
(85, 4, 17, 3, 'ENSALADA VERDURAS', 'N/A\r'),
(86, 4, 18, 3, 'LACTEOS', 'SORBETE DE MANGO\r'),
(87, 4, 18, 3, 'ALIMENTO PROTEICO', 'HUEVO REVUELTO\r'),
(88, 4, 18, 3, 'DERIVADO CEREAL', 'ARROZ CON FIDEOS\r'),
(89, 4, 18, 3, 'FRUTA', 'MANZANA\r'),
(90, 4, 18, 3, 'ENSALADA VERDURAS', 'ENS LECHUGA Y TOMATE'),
(91, 4, 19, 3, 'LACTEOS', 'REFRESCO DE AVENA\r'),
(92, 4, 19, 3, 'ALIMENTO PROTEICO', 'FAJITAS DE CERDO CON AHUYAMA Y ARVEJA\r'),
(93, 4, 19, 3, 'DERIVADO CEREAL', 'ARROZ BLANCO Y PAPA CRIOLLA DORADA\r'),
(94, 4, 19, 3, 'FRUTA', 'N/A\r'),
(95, 4, 19, 3, 'ENSALADA VERDURAS', 'N/A\r'),
(96, 4, 20, 3, 'LACTEOS', 'SORBETE DE GUAYABA\r'),
(97, 4, 20, 3, 'ALIMENTO PROTEICO', 'N/A\r'),
(98, 4, 20, 3, 'DERIVADO CEREAL', 'ESPAGUETIS EN SALSA BLANCA CON QUESO\r'),
(99, 4, 20, 3, 'FRUTA', 'PAPAYA PICADA\r'),
(100, 4, 20, 3, 'ENSALADA VERDURAS', 'ENS ESPINACA LECHUGA Y ZANAHORIA\r');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `puntaje_cumplimiento`
--

CREATE TABLE `puntaje_cumplimiento` (
  `id_puntaje` int(11) NOT NULL,
  `verificacion_menu_id` int(11) NOT NULL,
  `puntaje` float NOT NULL,
  `clasificacion` varchar(10) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `respuestas_bodega`
--

CREATE TABLE `respuestas_bodega` (
  `id_respuesta` int(11) NOT NULL,
  `id_visita` int(11) NOT NULL,
  `id_pregunta` int(11) NOT NULL,
  `respuesta` enum('0','1','2') NOT NULL,
  `observacion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `respuestas_infraestructura`
--

CREATE TABLE `respuestas_infraestructura` (
  `id_respuesta` int(11) NOT NULL,
  `id_pregunta` int(11) NOT NULL,
  `respuesta` tinyint(4) NOT NULL,
  `observacion` text DEFAULT NULL,
  `id_infraestructura` int(11) NOT NULL,
  `descripcion` varchar(500) DEFAULT NULL,
  `foto` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `respuestas_tecnica`
--

CREATE TABLE `respuestas_tecnica` (
  `id_respuesta` int(11) NOT NULL,
  `visita_tecnica_id` int(11) NOT NULL,
  `pregunta_id` int(11) NOT NULL,
  `respuesta` varchar(50) NOT NULL,
  `observaciones` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sedes`
--

CREATE TABLE `sedes` (
  `id_sede` int(11) NOT NULL,
  `nombre_sede` varchar(255) NOT NULL,
  `id_institucion` int(11) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `codigo` varchar(5) NOT NULL,
  `comuna` int(11) NOT NULL,
  `zona` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sedes`
--

INSERT INTO `sedes` (`id_sede`, `nombre_sede`, `id_institucion`, `direccion`, `codigo`, `comuna`, `zona`) VALUES
(1, '01/01 JOSE HOLGUIN GARCES  - BARRIO TERRON COLORADO', 1, 'AV. 4 OESTE NO 23-108 TERRON COLORADO ', '01/01', 1, 'URBANO'),
(2, '01/02 IE ANA MARIA LLOREDA', 1, 'CALLE 26 -AV 4 OESTE TERRON COLORADO', '01/02', 1, 'URBANO'),
(3, '01/03 IE JOSE ACEVEDO Y GOMEZ', 1, 'AV 5  OESTE # 30-164 TERRON COLORADO', '01/03', 1, 'URBANO'),
(4, '01/04 IE MARICE SINISTERRA', 1, 'CL 30 BIS OESTE # 4A-00', '01/04', 1, 'URBANO '),
(5, '01/05 IE ULPIANO LLOREDA', 1, 'AV 4B OESTE # 25-08 TERRON COLORADO', '01/05', 1, 'URBANO '),
(6, '01/06 IE VILLA DEL MAR', 1, 'AV. 8 OESTE # 30C-40', '01/06', 1, 'URBANO '),
(7, '02/01 IE ISAIAS GAMBOA', 2, 'AV. 4 OESTE  12 - 05', '02/01', 1, 'URBANO\r'),
(8, '02/02 LA INMACULADA', 2, 'CALLE 10 OESTE 05 - 45', '02/02', 1, 'URBANO\r'),
(9, '02/03 ALEJANDRO CABAL POMBO', 2, 'CALLE 26 OESTE 8 - 17', '02/03', 1, 'URBANO\r'),
(10, '02/04 JOSE CELESTINO MUTIS', 2, 'AV 7B OESTE 18 - 02', '02/04', 1, 'URBANO\r'),
(11, '02/05 EL AGUACATAL', 2, 'KM 2 VIA AGUACATAL', '02/05', 1, 'URBANO\r'),
(12, '03/01 IE LUIS FERNANDO CAICEDO - SEDE PRINCIPAL', 3, 'AV 5A OESTE 47A - 04', '03/01', 1, 'URBANO\r'),
(13, '03/02 CECILIA CABALLERO DE LOPEZ', 3, 'AV 5A OESTE 34 - 100', '03/02', 1, 'URBANO\r'),
(14, '04/01 IE TECNICO DE COMERCIO SANTA CECILIA 1', 4, 'CALLE 61A NORTE  2GN - 62', '04/01', 2, 'URBANO\r'),
(15, '04/03 REPUBLICA DE FRANCIA', 4, 'AV 2CN NO. 62N - 30', '04/03', 2, 'URBANO\r'),
(16, '04/04 BRISAS DE LOS ALAMOS', 4, 'AV 2BN NO. 72AN ESQUINA', '04/04', 2, 'URBANO\r'),
(17, '04/05 REPUBLICA  DE BRASIL', 4, 'CALLE 43 NORTE 7N-03', '04/05', 2, 'URBANO\r'),
(18, '04/06 REPUBLICA  DE BRASIL ALTO MENGA', 4, 'CALLE 53A NORTE 8 -27', '04/06', 2, 'URBANO\r'),
(19, '04/07 LA INMACULADA - BATACLAN', 4, 'AV. 10BN NO. 12B - 47', '04/07', 2, 'URBANO\r'),
(20, '05/01 IE DE SANTA LIBRADA', 5, 'CALLE 7 NO. 14A - 106', '05/01', 3, 'URBANO\r'),
(21, '05/02 CARLOS A.SARDI G.', 5, 'CRA. 5 NO. 2 - 69', '05/02', 3, 'URBANO\r'),
(22, '05/03 LUIS CARLOS PENA', 5, 'CALLE 7 NO. 14 - 36', '05/03', 3, 'URBANO\r'),
(23, '05/04 SANTIAGO DE CALI', 5, 'CALLE 17  7-74', '05/04', 3, 'URBANO\r'),
(24, '05/06 REPUBLICA DE MEXICO', 5, 'CALLE 20  5-65', '05/06', 3, 'URBANO\r'),
(25, '05/07 EL PILOTO', 5, 'CRA. 4NORTE  24-40', '05/07', 3, 'URBANO\r'),
(26, '05/08 EUSTAQUIO PALACIOS - BARRIO SAN ANTONIO', 5, 'CRA. 17 3A - 55', '05/08', 3, 'URBANO\r'),
(27, '06/01 IE NORMAL SUPERIOR FARALLONES DE CALI', 6, 'CRA 22 NO. 2-65 OESTE', '06/01', 3, 'URBANO\r'),
(28, '06/02 MARTIN RESTREPO MEJIA', 6, 'CRA 22 OESTE 2 - 65', '06/02', 3, 'URBANO\r'),
(29, '06/03 SALVADOR IGLESIAS', 6, 'CALLE 2A NO. 22-70', '06/03', 3, 'URBANO\r'),
(30, '06/05 FRANCISCO JOSE DE CALDAS', 6, 'CRA. 4 OESTE NO. 12A - 59', '06/05', 3, 'URBANO\r'),
(31, '06/07 MARIA PERLAZA', 6, 'CALLE 1ESTE NO. 18-02', '06/07', 3, 'URBANO\r'),
(32, '06/08 MANUEL SINISTERRA PATINO', 6, 'CRA 14 CON CALLE 3 OESTE', '06/08', 3, 'URBANO\r'),
(33, '07/01 IE JORGE ISAACS - INEM', 7, 'CRA 5 NORTE NO. 61 - 126', '07/01', 4, 'URBANO\r'),
(34, '07/02 CECILIA MUNOZ RICAURTE', 7, 'CLLE 77N  CRA 8N', '07/02', 4, 'URBANO\r'),
(35, '07/03 LAS AMERICAS - BARRIO FLORALIA', 7, 'CLLE 82  3AN -03', '07/03', 4, 'URBANO\r'),
(36, '07/04 FRAY DOMINGO DE LAS CASAS', 7, 'CLLE 65N  6N-40', '07/04', 4, 'URBANO\r'),
(37, '07/05 CENTRO EDUCATIVO DEL NORTE', 7, 'CRA 4N  51– AN 33', '07/05', 4, 'URBANO\r'),
(38, '07/06 CAMILO TORRES', 7, 'CRA 9N  56BN -57', '07/06', 4, 'URBANO\r'),
(39, '07/07 PABLO EMILIO CAICEDO', 7, 'CRA 5N DG 7N -39', '07/07', 4, 'URBANO\r'),
(40, '08/01 IE GUILLERMO VALENCIA', 8, 'CRA 7 NORTE NO 45A08', '08/01', 4, 'URBANO\r'),
(41, '08/02 PRESBITERO ANGEL PIEDRAHITA', 8, 'CRA 8 NORTE NO 51N 35', '08/02', 4, 'URBANO\r'),
(42, '09/01 IE REPUBLICA DE ISRAEL', 9, 'CRA. 3 # 43-49', '09/01', 4, 'URBANO\r'),
(43, '09/02 MANUEL SANTIAGO VALLECILLA', 9, 'CALLE 43 # 4 B-33', '09/02', 4, 'URBANO\r'),
(44, '09/03 SAN JOSE', 9, 'CALLE 40 # 2C - 21', '09/03', 4, 'URBANO\r'),
(45, '10/01 IE SANTO TOMAS  CASD', 10, 'CALLE 34 # 3N-15', '10/01', 4, 'URBANO\r'),
(46, '10/02  SANTO TOMAS DE AQUINO', 10, 'CLLE. 33 # 2N-11', '10/02', 4, 'URBANO\r'),
(47, '10/03  MANUELA BELTRAN', 10, 'CRA. 1h # 34-64', '10/03', 4, 'URBANO\r'),
(48, '10/04 JORGE ISAACS', 10, 'CLLE 30  # 5-88', '10/04', 4, 'URBANO\r'),
(49, '11/01 IE TECNICO INDUSTRIAL VEINTE DE JULIO', 11, 'CARRERA 5 NORTE # 33-01', '11/01', 4, 'URBANO\r'),
(50, '11/02 IGNACIO RENGIFO', 11, 'CALLE 41 NORTE 5N-23', '11/02', 4, 'URBANO\r'),
(51, '11/03  CRISTINA SERRANO', 11, 'CARRERA 5 NORTE 33-00', '11/03', 4, 'URBANO\r'),
(52, '11/04 ADAN CORDOVEZ CORDOBA', 11, 'Cra. 5 #34-15', '11/04', 4, 'URBANO\r'),
(53, '12/01 IE JOSE ANTONIO GALAN', 12, 'CALLE 41 NO. 3N-11', '12/01', 4, 'URBANO\r'),
(54, '12/02 RAFAEL ZAMORANO', 12, 'CRA. 2 NORTE  NO. 45A - 12', '12/02', 4, 'URBANO\r'),
(55, '13/01 IE LA MERCED', 13, 'CALLE 47 # 4E-30', '13/01', 4, 'URBANO\r'),
(56, '13/02 SAN VICENTE DE PAUL', 13, 'CARRERA 2B  NO. 45A - 20', '13/02', 4, 'URBANO\r'),
(57, '13/03 SAN PEDRO ALEJANDRINO', 13, 'CARRERA 4E  NO. 46A - 04', '13/03', 4, 'URBANO\r'),
(58, '13/04 CENDOE', 13, 'CALLE 44A  NO. 4B - 00', '13/04', 4, 'URBANO\r'),
(59, '14/01 SIMON RODRIGUEZ - BARRIO SENA', 14, 'CARRERA 1D BIS # 49-98', '14/01', 5, 'URBANO\r'),
(60, '14/02 MARIA PANESSO', 14, 'CALLE 46C# 3-00', '14/02', 5, 'URBANO\r'),
(61, '14/03 MARIO LLOREDA', 14, 'CRA 1D # 51-16', '14/03', 5, 'URBANO\r'),
(62, '15/01 IE CELMIRA BUENO DE OREJUELA', 15, 'CALLE 62B Nº 1A-9-250', '15/01', 5, 'URBANO\r'),
(63, '15/02 MARIANO OSPINA PEREZ', 15, 'CALLE 67 NO. 2 - 00', '15/02', 5, 'URBANO\r'),
(64, '16/01 IETI PEDRO ANTONIO MOLINA', 16, 'CRA 1A 10 #71 00', '16/01', 6, 'URBANO\r'),
(65, '16/02 TRES DE JULIO', 16, 'CLL 70C CRA 1F - 00', '16/02', 6, 'URBANO\r'),
(66, '16/03 SAN JORGE', 16, 'CRA 1 A1 #74 23', '16/03', 6, 'URBANO\r'),
(67, '16/04  JORGE ELIECER GAITAN - BARRIO JORGE ELIECER GAITAN', 16, 'CRA 2C1 # 71 00', '16/04', 6, 'URBANO\r'),
(68, '16/05 SAN LUIS', 16, 'CALLE 72 No. 1B - 03', '16/05', 6, 'URBANO\r'),
(69, '16/06  INMACULADA CONCEPCION', 16, 'CLL 73A #1A 14 21', '16/06', 6, 'URBANO\r'),
(70, '16/07 ATANASIO GIRARDOT', 16, 'CRA 1 A3 #70B 00', '16/07', 6, 'URBANO\r'),
(71, '16/08 LOS VENCEDORES', 16, 'CRA 1A 4 #72D 19', '16/08', 6, 'URBANO\r'),
(72, '17/01 IE MANUEL MARIA MALLARINO - BARRIO LAS CEIBAS', 17, 'CRA 7 L  BIS NO. 63-00', '17/01', 7, 'URBANO\r'),
(73, '17/02 LAURA VICUNA', 17, 'CRA 7L BIS NO. 63-00', '17/02', 7, 'URBANO\r'),
(74, '17/03  LOS PINOS', 17, 'CALLE 69A NO. 7M BIS 00', '17/03', 7, 'URBANO\r'),
(75, '17/04 CARLOS HOLGUIN SARDI', 17, 'PASAJE 7D BIS 64-00', '17/04', 7, 'URBANO\r'),
(76, '18/01 JUAN BAUTISTA DE LA SALLE', 18, 'CALLE 74 # 9-19', '18/01', 7, 'URBANO\r'),
(77, '18/02 MANUEL MARIA MALLARINO - BARRIO PUERTO MALLARINO', 18, 'CARRERA 9 A # 78-14', '18/02', 7, 'URBANO\r'),
(78, '19/01 IE VICENTE BORRERO COSTA', 19, 'CALLE 76N NO. 7S - 00', '19/01', 7, 'URBANO\r'),
(79, '19/02 PEBRO ELOY VALENZUELA', 19, 'CALLE 74 NO.7P BIS - 46', '19/02', 7, 'URBANO\r'),
(80, '19/03 JOSE MARIA VILLEGAS', 19, 'CALLE 82 CRA 7D-1', '19/03', 7, 'URBANO\r'),
(81, '19/04 ALFONSO LOPEZ PUMAREJO - BARRIO ALFONSO LOPEZ  III', 19, 'CALLE 84 CRA 7ABIS ESQUINA', '19/04', 7, 'URBANO\r'),
(82, '20/01 IE  SIETE DE AGOSTO', 20, 'CALLE 72 # 11C - 27', '20/01', 7, 'URBANO\r'),
(83, '20/02 ELEAZAR LIBREROS', 20, 'CALLE 72B DIAG 12', '20/02', 7, 'URBANO\r'),
(84, '20/03 UNIDAD VECINAL SIETE DE AGOSTO', 20, 'CALLE 71A DIAG 17 - 20', '20/03', 7, 'URBANO\r'),
(85, '21/01 IE JUAN DE AMPUDIA', 21, 'CRA. 12 # 57-13', '21/01', 8, 'URBANO\r'),
(86, '21/02 JARDIN NACIONAL NO.1', 21, 'CALLE 58 # 11B-48', '21/02', 8, 'URBANO\r'),
(87, '21/03 ONCE DE NOVIEMBRE', 21, 'CRA. 11D # 52-09', '21/03', 8, 'URBANO\r'),
(88, '22/01 IE VILLACOLOMBIA', 22, 'CR 12E N° 48 36', '22/01', 8, 'URBANO\r'),
(89, '22/02 SANTISIMA TRINIDAD', 22, 'CALLE 48 NO. 12 - 84', '22/02', 8, 'URBANO\r'),
(90, '22/03 REPUBLICA DE COLOMBIA', 22, 'CALLE 53 NO. 12E - 11', '22/03', 8, 'URBANO\r'),
(91, '23/01 IE LAS AMERICAS - BARRIO AMERICAS', 23, 'CARRERA 12 38-58', '23/01', 8, 'URBANO\r'),
(92, '23/03 NTRA SRA DE LORETO', 23, 'CRA 8 NO. 38 - 55', '23/03', 8, 'URBANO\r'),
(93, '23/04 GABRIEL MONTANO', 23, 'CRA 11C NO. 38 - 60', '23/04', 8, 'URBANO\r'),
(94, '23/05 ATANACIO GIRARDOT', 23, 'KR 11 B 35 00', '23/05', 8, 'URBANO\r'),
(95, '23/06  RAFAEL URIBE URIBE', 23, 'CARRERA 12 38-59', '23/06', 8, 'URBANO\r'),
(96, '24/01 JOSE MANUEL SAAVEDRA GALINDO', 24, 'CRA. 11 A NO. 28-25', '24/01', 8, 'URBANO\r'),
(97, '24/02 NUESTRA SENORA DE FATIMA', 24, 'CRA 10 NO. 28-10', '24/02', 8, 'URBANO\r'),
(98, '24/03 BENJAMIN HERRERA', 24, 'CLL 26 NO. 12-34', '24/03', 8, 'URBANO\r'),
(99, '25/01 ALBERTO CARVAJAL BORRERO', 25, 'CRA 14  # 58 - 00', '25/01', 8, 'URBANO\r'),
(100, '25/02 ABRAHAN DOMINGUEZ', 25, 'CRA 14 # 57 - 19', '25/02', 8, 'URBANO\r'),
(101, '25/03 CACIQUE DE GUATAVITA', 25, 'CALLE 54 # 15A - 20', '25/03', 8, 'URBANO\r'),
(102, '26/01 IE EVARISTO GARCIA ', 26, 'CALLE 32 NO. 17 - 41', '26/01', 8, 'URBANO\r'),
(103, '26/02 SAAVEDRA GALINDO', 26, 'CARRERA 17F  TRANSV 31 - 00', '26/02', 8, 'URBANO\r'),
(104, '26/03 FERNANDO DE ARAGON', 26, 'CALLE 28A DIAGONAL 20-00', '26/03', 8, 'URBANO\r'),
(105, '26/04 JOSE HILARIO LOPEZ', 26, 'CALLE 27 N° 17G-19', '26/04', 8, 'URBANO\r'),
(106, '27/01 IE SANTA FE', 27, 'CALLE  34  NO. 17B - 41', '27/01', 8, 'URBANO\r'),
(107, '27/02 RICARDO NIETO', 27, 'CARRERA 17 CON CALLE 36', '27/02', 8, 'URBANO\r'),
(108, '27/03 CROYDON', 27, 'N/A', '27/03', 8, 'URBANO\r'),
(109, '27/04  PUERTO RICO', 27, 'CARRERA 17 #  33D - 01', '27/04', 8, 'URBANO\r'),
(110, '27/05 MANUEL REBOLLEDO', 27, 'Cra 17f # dg 23', '27/05', 8, 'URBANO\r'),
(111, '28/01 IE REPUBLICA DE ARGENTINA', 28, 'CARRERA 11 D NO. 23-49', '28/01', 9, 'URBANO\r'),
(112, '28/02 POLICARPA SALAVARRIETA - BARRIO OBRERO', 28, 'CARRERA 11 NO. 22A-30', '28/02', 9, 'URBANO\r'),
(113, '28/03 JOSE MARIA CORDOBA', 28, 'CALLE 18 NO. 8A-15', '28/03', 9, 'URBANO\r'),
(114, '28/04 SEBASTIAN DE BELALCAZAR', 28, 'CALLE 17 NO. 14-57', '28/04', 9, 'URBANO\r'),
(115, '29/01 IE  ANTONIO JOSE CAMACHO', 29, 'CRA 16 NO. 12-00', '29/01', 9, 'URBANO\r'),
(116, '29/02 REPUBLICA DEL PERU', 29, 'CALLE 9E NO. 23-02', '29/02', 9, 'URBANO\r'),
(117, '29/03 MARCO FIDEL SUAREZ', 29, 'KR 16 NO. 6 - 61', '29/03', 9, 'URBANO\r'),
(118, '29/04 JARDIN INFANTIL DIVINO SALVADOR', 29, 'KR 15 NO. 6 - 110', '29/04', 9, 'URBANO\r'),
(119, '29/05 OLGA LUCIA LLOREDA', 29, 'CRA 23A NO. 13B - 11', '29/05', 9, 'URBANO\r'),
(120, '30/01 IE GENERAL ALFREDO VASQUEZ COBO - BARRIO ARANJUEZ', 30, 'CALLE 15A NO. 22A - 37', '30/01', 9, 'URBANO\r'),
(121, '30/02 REPUBLICA DEL ECUADOR', 30, 'CL. 16 NO. 18A - 54', '30/02', 9, 'URBANO\r'),
(122, '30/03 NUESTRA SENORA DE LOS REMEDIOS', 30, 'CRA.17 D NO. 18 - 46', '30/03', 9, 'URBANO\r'),
(123, '31/01 IE NORMAL SUPERIOR SANTIAGO DE CALI', 31, 'CRA 33A #12-60', '31/01', 10, 'URBANO\r'),
(124, '31/02 JOAQUIN CAYCEDO Y CUERO', 31, 'CR 36 # 12C-00', '31/02', 10, 'URBANO\r'),
(125, '32/01 JOSE MARIA CARBONELL - BARRIO PASOANCHO', 32, 'CALLE 13 Nº 32 - 88', '32/01', 10, 'URBANO\r'),
(126, '32/02 HONORIO VILLEGAS', 32, 'CARRERA 35 # 13A - 20', '32/02', 10, 'URBANO\r'),
(127, '32/03 ISABEL DE CASTILLA', 32, 'CRA 33 No. 15-82', '32/03', 10, 'URBANO\r'),
(128, '33/01 IE JOAQUIN DE CAYZEDO Y CUERO', 33, 'CRA 35 # 15-33', '33/01', 10, 'URBANO\r'),
(129, '33/02 SATELITE CAMILO TORRES', 33, 'CRA 24 # 10A-98', '33/02', 10, 'URBANO\r'),
(130, '33/03 SAN ROQUE', 33, 'CRA 32A #15A-59', '33/03', 10, 'URBANO\r'),
(131, '33/04 GENERAL CARLOS ALBAN', 33, 'CALLE 18A # 24-65', '33/04', 10, 'URBANO\r'),
(132, '34/01 IE RAFAEL NAVIA VARON', 34, 'CLL 14 #48A-32', '34/01', 10, 'URBANO\r'),
(133, '34/02 FRANCISCO MONTES IDROBO', 34, 'CALLE 12 # 46 - 40', '34/02', 10, 'URBANO\r'),
(134, '34/03 PANAMERICANA', 34, 'CALLE 12A No. 48 - 12', '34/03', 10, 'URBANO\r'),
(135, '35/01 IE JOSE MARIA VIVAS BALCAZAR - BARRIO LA SELVA', 35, 'CLL 14 #48A-32', '35/01', 10, 'URBANO\r'),
(136, '35/02 SANTO DOMINGO - BARRIO LA SELVA', 35, 'CRA 47 NO.13C - 100', '35/02', 10, 'URBANO\r'),
(137, '35/03 FERNANDO VELASCO', 35, 'CALLE 23 # 44A-16', '35/03', 10, 'URBANO\r'),
(138, '36/01 IE CARLOS HOLGUIN LLOREDA', 36, 'CRA. 40  NO. 18-85', '36/01', 10, 'URBANO\r'),
(139, '36/02 REPUBLICA DE COSTA RICA', 36, 'CRA. 41A NO. 14C - 00', '36/02', 10, 'URBANO\r'),
(140, '36/03 SANTA ELENA', 36, 'CALLE 23 NO. 32  79', '36/03', 10, 'URBANO\r'),
(141, '36/04 JARDIN INFANTIL NACIONAL NO. 2', 36, 'CRA 42 A NO. 14 B 15', '36/04', 10, 'URBANO\r'),
(142, '37/01 IE AGUSTIN NIETO CABALLERO', 37, 'KRA. 37 # 26C-51', '37/01', 11, 'URBANO\r'),
(143, '37/02 MARINO RENGIFO SALCEDO', 37, 'CALLE 26C # 44-00', '37/02', 11, 'URBANO\r'),
(144, '37/03 JOSE MARIA VIVAS BALCAZAR - BARRIO EL JARDIN', 37, 'CARRERA 36 #26B-28', '37/03', 11, 'URBANO\r'),
(145, '37/04 ANTONIO RICAURTE', 37, 'CALLE 26B CON CARRERA 46', '37/04', 11, 'URBANO\r'),
(146, '38/01 IE BOYACA', 38, 'CRA. 33A No. 25 - 25', '38/01', 11, 'URBANO\r'),
(147, '38/02  LA INDEPENDENCIA', 38, 'CRA. 39 No. 26C - 30', '38/02', 11, 'URBANO\r'),
(148, '38/03  SANTO DOMINGO', 38, 'CRA. 29A No. 26B - 64', '38/03', 11, 'URBANO\r'),
(149, '39/01 IE DIEZ DE MAYO', 39, 'CARRERA 25 A No. 26A-13', '39/01', 11, 'URBANO\r'),
(150, '39/02 CENTRO DOCENTE REPUBLICA DE ITALIA', 39, 'CARRERA 24B CON CALLE 26B', '39/02', 11, 'URBANO\r'),
(151, '40/01 IE VILLA DEL SUR', 40, 'CLL 30A N 41E - 99', '40/01', 11, 'URBANO\r'),
(152, '40/02 SUSANA VINASCO DE QUINTANA', 40, 'CALLE 31 Nª33 A 00', '40/02', 11, 'URBANO\r'),
(153, '41/01 IE CIUDAD MODELO', 41, 'CARRERA 40 B No. 31C - 00', '41/01', 11, 'URBANO\r'),
(154, '41/02 PRIMAVERA', 41, 'CRA 35  # 34 C - 21', '41/02', 11, 'URBANO\r'),
(155, '42/01 IE GENERAL FRANCISCO DE PAULA SANTANDER - BARRIO EL JARDIN', 42, 'CALLE 27 31A-60 B/EL JARDIN', '42/01', 11, 'URBANO\r'),
(156, '42/02 JOSE VICENTE CONCHA', 42, 'CRA 30A 30A-27', '42/02', 11, 'URBANO\r'),
(157, '42/03 SAN PEDRO CODENAL', 42, 'CRA 31 DG 31-10', '42/03', 11, 'URBANO\r'),
(158, '42/04 LEON XIII', 42, 'Cl 35 Kr 29 B', '42/04', 11, 'URBANO\r'),
(159, '42/05 JULIO ARBOLEDA', 42, 'CL 35E 30-24', '42/05', 11, 'URBANO\r'),
(160, '43/01 IE COMERCIAL CIUDAD DE CALI', 43, 'CALLE 30 # 25-00', '43/01', 11, 'URBANO\r'),
(161, '43/02 GENERAL ALFREDO VASQUEZ COBO - BARRIO 20 DE JULIO', 43, 'DIG. 23 Nº. T25-25', '43/02', 11, 'URBANO\r'),
(162, '43/03 EL RECUERDO', 43, 'CRA 27 Nº. 29-25', '43/03', 11, 'URBANO\r'),
(163, '44/01 IE EVA RIASCOS PLATA', 44, 'TRANVERSAL 25 DIAG. 26 - 69', '44/01', 12, 'URBANO\r'),
(164, '44/02 ALFONSO BARBERENA', 44, 'CRA. 25 BIS No. 33C - 25 ESQ.', '44/02', 12, 'URBANO\r'),
(165, '44/03 HERNANDO CAICEDO', 44, 'TRANS 29 DIAG. 27A - 00', '44/03', 12, 'URBANO\r'),
(166, '45/01 IE TECNICA COMERCIAL HERNANDO NAVIA VARON', 45, 'CRA 26P # 50-39', '45/01', 12, 'URBANO\r'),
(167, '45/02 FRAY JOSE IGNACIO ORTIZ', 45, 'CRA 26N # 52-58', '45/02', 12, 'URBANO\r'),
(168, '46/01 IE JUAN XXIII', 46, 'CARRERA 28 C 50 - 16', '46/01', 12, 'URBANO\r'),
(169, '46/02 INST EDUC   CIUDAD DE CALI.', 46, 'CALLE 46 28F 31', '46/02', 12, 'URBANO\r'),
(170, '46/03 CENTRO DOCENTE NINO JESUS DE PRAGA', 46, 'CARRERA  28 C 44 - 90', '46/03', 12, 'URBANO\r'),
(171, '46/04 CENTRO DOCENTE JULIO RINCON', 46, 'CALLE 70  28 E BIS - 00', '46/04', 12, 'URBANO\r'),
(172, '46/05 BELLO HORIZONTE', 46, 'CALLE 36 A 27 A 30', '46/05', 12, 'URBANO\r'),
(173, '46/06 SAN BUENAVENTURA', 46, 'DG  29B # TRANSV. 29-30', '46/06', 12, 'URBANO\r'),
(174, '47/01 IE JULIO CAICEDO Y TELLEZ', 47, 'calle 59 N. 24E-40', '47/01', 12, 'URBANO\r'),
(175, '47/02 BATALLA DE CARABOBO', 47, 'Calle 51 # 16-00', '47/02', 12, 'URBANO\r'),
(176, '47/03 FRANCISCO DE PAULA SANTANDER - BARRIO NUEVA FLORESTA', 47, 'CRA 26 H 50-53', '47/03', 12, 'URBANO\r'),
(177, '47/04 STHER ZORRILLA', 47, 'CALLE 59 #  24-00', '47/04', 12, 'URBANO\r'),
(178, '47/05 MI BOSQUESITO', 47, 'CALLE 57 #24A 03', '47/05', 12, 'URBANO\r'),
(179, '48/01 IE INDUSTRIAL MARICE SINISTERRA', 48, 'CALLE 39 # 25A - 43', '48/01', 12, 'URBANO\r'),
(180, '48/02 ASTURIAS', 48, 'CRA. 24B #43-40', '48/02', 12, 'URBANO\r'),
(181, '48/03 FENALCO ASTURIAS', 48, 'CALLE 44 #25A - 12', '48/03', 12, 'URBANO\r'),
(182, '49/01 IE BARTOLOME LOBOGUERRERO', 49, 'CALLE 71 Nº 26E-25', '49/01', 13, 'URBANO\r'),
(183, '49/02 ENRIQUE OLAYA HERRERA - BARRIO ULPIANO LLOREDA', 49, 'CALLE 71 Nº 25A-15', '49/02', 13, 'URBANO\r'),
(184, '50/01 IE HUMBERTO JORDAN MAZUERA', 50, 'CRA 26 I #  D71A-25', '50/01', 13, 'URBANO\r'),
(185, '50/02 MIGUEL CAMACHO PEREA', 50, 'CRA. 28A No. 72F-09', '50/02', 13, 'URBANO\r'),
(186, '50/03 VILLABLANCA', 50, 'DIAG. 72F No. 28A-05', '50/03', 13, 'URBANO\r'),
(187, '50/04 CHARCO AZUL', 50, 'DIAG.70B1 No. 22B Bis-', '50/04', 13, 'URBANO\r'),
(188, '51/01 IE JESUS VILLAFANE FRANCO', 51, 'CALLE 72 P TRANSV. 72 S ESQUIN', '51/01', 13, 'URBANO\r'),
(189, '51/02 OMAIRA SANCHEZ', 51, 'TRANV.72W #72O - 08', '51/02', 13, 'URBANO\r'),
(190, '52/01 IE SANTA ROSA SEDE  I', 52, 'CALLE 72 X Nº 28-3 - 35', '52/01', 13, 'URBANO\r'),
(191, '52/02 JOSE CARDONA HOYOS', 52, 'CALLE 72N Nº 28- 130', '52/02', 13, 'URBANO\r'),
(192, '53/01 IE TECNICO INDUSTRIAL LUZ HAYDEE GUERRERO', 53, 'CARRERA 28E2 No. 72S - 02', '53/01', 13, 'URBANO\r'),
(193, '53/02 CENTRO DOCENTE RODRIGO LLOREDA CAICEDO - BARRIO POBLADO I', 53, 'CRA 30  No. 44A - 21 B/EL POBLADO I', '53/02', 13, 'URBANO\r'),
(194, '54/01 IE  EL DIAMANTE', 54, 'CARRERA 31 No. 41-00', '54/01', 13, 'URBANO\r'),
(195, '54/02 JUAN PABLO II - BARRIO EL VERGEL', 54, 'KRA. 33 Nº 42C - 09', '54/02', 13, 'URBANO\r'),
(196, '54/03 SEÑOR DE LOS MILAGROS (EL RETIRO)', 54, 'Cra 38 # 51a-02', '54/03', 15, 'URBANO\r'),
(197, '55/01 IE MONSENOR RAMON ARCILA', 55, 'DIAGONAL 26 I3 TRANSV. 80A-18', '55/01', 14, 'URBANO\r'),
(198, '55/02 RAUL SILVA HOLGUIN', 55, 'DG 26K TRANSV. 83 - 24', '55/02', 14, 'URBANO\r'),
(199, '55/03 ALFONSO REYES ECHANDIA', 55, 'DG 26 P16 No.105-04', '55/03', 14, 'URBANO\r'),
(200, '55/04 PUERTAS DEL SOL IV Y V', 55, 'DIAG. 108 No. 26I - 40', '55/04', 14, 'URBANO\r'),
(201, '56/01 IE LA ANUNCIACION', 56, 'CRA 26 A No. 74-00', '56/01', 14, 'URBANO\r'),
(202, '56/02  LOS NARANJOS', 56, 'DIAG. 26G1 No. 78 - 00', '56/02', 14, 'URBANO\r'),
(203, '56/03  PUERTA DEL SOL', 56, 'CALLE 84 # 26 C - 04', '56/03', 14, 'URBANO\r'),
(204, '57/01 IE GABRIELA MISTRAL', 57, 'CALLE 95 CRA. 27D ESQUINA', '57/01', 14, 'URBANO\r'),
(205, '57/02 ISAIAS HERNAN IBARRA', 57, 'CRA 27F CLS 112 Y 113', '57/02', 14, 'URBANO\r'),
(206, '57/03 ELIAS SALAZAR GARCIA', 57, 'CRA 26 I CALLES 106- 108', '57/03', 14, 'URBANO\r'),
(207, '57/04 DAMASO ZAPATA', 57, 'CALLE 92 #  28 C 12', '57/04', 14, 'URBANO\r'),
(208, '58/01 IEGABRIEL GARCIA MARQUEZ ', 58, 'CRA 29B #54-00', '58/01', 15, 'URBANO\r'),
(209, '58/02 JOSE RAMON BEJARANO', 58, 'CRA 32A #49-00', '58/02', 15, 'URBANO\r'),
(210, '58/04 ALFONSO BONILLA NAAR', 58, 'CALLE 57 #33-11', '58/04', 15, 'URBANO\r'),
(211, '59/01 IECARLOS HOLGUIN MALLARINO', 59, 'CALLE 55A # 30B-50', '59/01', 15, 'URBANO\r'),
(212, '59/02 NINO JESUS DE ATOCHA', 59, 'CALLE 83 #28E3 -05', '59/02', 15, 'URBANO\r'),
(213, '59/03 MIGUEL DE POMBO', 59, 'CALLE 92 #28D4 - 13', '59/03', 15, 'URBANO\r'),
(214, '59/04 EL RETIRO', 59, 'Cra. 37 #54-39 a 54-1', '59/04', 15, 'URBANO\r'),
(215, '60/01 IE CIUDAD CORDOBA', 60, 'CALLE 50 # 49C-100', '60/01', 15, 'URBANO\r'),
(216, '60/02 ENRIQUE OLAYA HERRERA - BARRIO EL VALLADO', 60, 'CALLE 51 No. 40A - 08', '60/02', 15, 'URBANO\r'),
(217, '61/01 IE RODRIGO LLOREDA CAICEDO - BARRIO MARIANO RAMOS', 61, 'CALLE 38A N. 47A-45 B/MARIANO RAMOS', '61/01', 16, 'URBANO\r'),
(218, '61/02 MICAELA CASTRO BORRERO', 61, 'CRA 46C No. 38A-27', '61/02', 16, 'URBANO\r'),
(219, '61/03 LUIS ENRIQUE MONTOYA', 61, 'CRA 46C No. 38A- 50', '61/03', 16, 'URBANO\r'),
(220, '61/04 PRIMITIVO CRESPO', 61, 'CALLE 47 No 51A-30', '61/04', 16, 'URBANO\r'),
(221, '62/01 IE CRISTOBAL COLON - BARRIO MARIANO RAMOS', 62, 'CL. 44 Nº 47A-00 B/MARIANO RAMOS', '62/01', 16, 'URBANO\r'),
(222, '62/02 BIENESTAR SOCIAL', 62, 'CRA. 47B No. 45 - 74', '62/02', 16, 'URBANO\r'),
(223, '62/03 ANTONIA SANTOS', 62, 'CRA 43 # 43 - 04', '62/03', 16, 'URBANO\r'),
(224, '62/04 JOSE JOAQUIN JARAMILLO', 62, 'CRA. 44 No. 44 - 64', '62/04', 16, 'URBANO\r'),
(225, '63/01 IE DONALD RODRIGO TAFUR', 63, 'CRA 43B #40-11', '63/01', 16, 'URBANO\r'),
(226, '63/02 FRANCISCO J. RUIZ', 63, 'CALLE 38 #43B-16', '63/02', 16, 'URBANO\r'),
(227, '63/03 ALEJANDRO MONTANO', 63, 'CRA. 41H #38-44', '63/03', 16, 'URBANO\r'),
(228, '63/04 ANTONIO NARINO', 63, 'CRA 40A #38-38', '63/04', 16, 'URBANO\r'),
(229, '63/05 JOSE MARIA CARBONELL - BARRIO ANTONIO NARIÑO', 63, 'CRA 39 #39D-83 B/ANTONIO NARIÑO', '63/05', 16, 'URBANO\r'),
(230, '64/01 IE LIBARDO MADRID VALDERRAMA', 64, 'CRA 41H No. 39-73', '64/01', 16, 'URBANO\r'),
(231, '64/02 ANGELICA SIERRA ARIZABALETA', 64, 'calle 40 No. 41F  esquina', '64/02', 16, 'URBANO\r'),
(232, '64/03 PABLO NERUDA', 64, 'Cra 39D No. 38 - 44', '64/03', 16, 'URBANO\r'),
(233, '64/04 PRIMERO DE MAYO', 64, 'Cra. 37 Calle 39 Esquina', '64/04', 16, 'URBANO\r'),
(234, '65/01 IE CARLOS HOLMES TRUJILLO', 65, 'CALLE 44 CARRERA 43', '65/01', 16, 'URBANO\r'),
(235, '65/02 POLICARPA SALAVARRIETA - BARRIO ANTONIO NARIÑO', 65, 'CALLE 44 CRA 40 B/ANTONIO NARIÑO', '65/02', 16, 'URBANO\r'),
(236, '65/03 LIZANDRO FRANKY', 65, 'CALLE 46 CRA 40', '65/03', 16, 'URBANO\r'),
(237, '65/04 CRISTO MAESTRO', 65, 'CALLE 44 CRA41F', '65/04', 16, 'URBANO\r'),
(238, '66/01 IE TECNICO INDUSTRIAL COMUNA DIECISIETE', 66, 'Cra 53 # 18 A-25', '66/01', 17, 'URBANO\r'),
(239, '66/02 LUIS CARLOS ROJAS GARCES', 66, 'CARRERA 56 # 13 F 40', '66/02', 17, 'URBANO\r'),
(240, '67/01 IE ALVARO ECHEVERRY', 67, 'CLL 4  NO. 92-04', '67/01', 18, 'URBANO\r'),
(241, '67/02 RUFINO JOSE CUERVO', 67, 'CLL 4 NO. 92-04', '67/02', 18, 'URBANO\r'),
(242, '67/03 LUIS EDUARDO NIETO CABALLERO', 67, 'CRA 92 NO. 4N - 119', '67/03', 18, 'URBANO\r'),
(243, '67/04 EDUARDO RIASCOS GRUESO', 67, 'CRA 93 NO. 2A - 02', '67/04', 18, 'URBANO\r'),
(244, '68/01 IE LA ESPERANZA', 68, 'CRA 94 NO. 1A - 71 OESTE', '68/01', 18, 'URBANO\r'),
(245, '68/02 MAGDALENA ORTEGA DE NARINO', 68, 'CL 4C OESTE NO. 94A - 54', '68/02', 18, 'URBANO\r'),
(246, '68/03 MONSENOR LUIS ADRIANO DIAZ', 68, 'CRA 94C NO. 2 - 111', '68/03', 18, 'URBANO\r'),
(247, '68/04  MINUTO DE DIOS', 68, 'PAMPAS DEL MIRADOR', '68/04', 18, 'URBANO\r'),
(248, '69/01 IE JUAN PABLO II BARRIO PRADOS DEL SUR', 69, 'CALLE 1A OESTE No. 78-23 B/PRADOS DEL SUR', '69/01', 18, 'URBANO\r'),
(249, '69/02 PORTETE DE TARQUI', 69, 'CALLE 1A OESTE Nº 73-00', '69/02', 18, 'URBANO\r'),
(250, '69/03 TEMPLO DEL SABER', 69, 'CALLE 2C OESTE Nº 75-10', '69/03', 18, 'URBANO\r'),
(251, '69/04  ALVARO ESCOBAR NAVIA', 69, 'CARRERA 73D Nº 1B - 65', '69/04', 18, 'URBANO\r'),
(252, '70/01 IE LICEO DEPARTAMENTAL', 70, 'CARRERA 37A 8-38', '70/01', 19, 'URBANO\r'),
(253, '70/02 LA PRESENTACION - BARRIO SAN FERNANDO', 70, 'CALLE 5B1 KRA 30 NO. 29-06', '70/02', 19, 'URBANO\r'),
(254, '70/03 LA GRAN COLOMBIA-LA GRAN COLOMBIA', 70, 'CARRERA 24  7-74', '70/03', 19, 'URBANO\r'),
(255, '71/01 IE POLITECNICO MUNICIPAL DE CALI', 71, 'CARRERA 62 2 - 28', '71/01', 19, 'URBANO\r'),
(256, '71/02 25 DE JULIO', 71, 'CALLE  6  59A - 51', '71/02', 19, 'URBANO\r'),
(257, '71/03  GENERAL SANTANDER - BARRIO BUENOS AIRES', 71, 'CALLE 5 70- 160', '71/03', 19, 'URBANO\r'),
(258, '71/04 JHON F. KENNEDY', 71, 'CARRERA 68 3- 83', '71/04', 19, 'URBANO\r'),
(259, '71/05 CELIMO RUEDA', 71, 'CARRERA 73 3 - 94', '71/05', 19, 'URBANO\r'),
(260, '72/01 IE EUSTAQUIO PALACIOS - BARRIO LIDO', 72, 'CRA. 52 # 2-51', '72/01', 19, 'URBANO\r'),
(261, '72/03 LUIS LOPEZ DE MESA', 72, 'CALLE 3 OESTE NO. 42 - 44', '72/03', 19, 'URBANO\r'),
(262, '72/04 SOFIA CAMARGO DE LLERAS', 72, 'CALLE 12A OESTE CRA. 51 OESTE', '72/04', 19, 'URBANO\r'),
(263, '72/05 GENERAL ANZOATEGUI', 72, 'CALLE 1A NO. 43 - 68', '72/05', 19, 'URBANO\r'),
(264, '72/06 SANTIAGO RENGIFO SALCEDO', 72, 'CALLE 23 OESTE NO. 47 - 06', '72/06', 19, 'URBANO\r'),
(265, '72/07 FRAY CRISTOBAL DE TORRES', 72, 'DIAG. 69 NO. 33 - 09', '72/07', 19, 'URBANO\r'),
(266, '72/08 MARISCAL JORGE ROBLEDO', 72, 'CARRERA 49 OESTE NO. 9 - 02', '72/08', 19, 'URBANO\r'),
(267, '72/09 MIGUEL ANTONIO CARO', 72, 'CALLE 6 OESTE CRA 42B ESQ', '72/09', 19, 'URBANO\r'),
(268, '72/10 MANUEL MARIA BUENAVENTURA', 72, 'CRA 4B OESTE NO. 6A - 52', '72/10', 19, 'URBANO\r'),
(269, '72/11 TULIO ENRIQUE TASCON', 72, 'KM 5 VIA CRISTO REY', '72/11', 19, 'URBANO\r'),
(270, '73/01 IE JUANA DE CAICEDO Y CUERO', 73, 'CALLE 1 OESTE NO50-85', '73/01', 19, 'URBANO\r'),
(271, '73/02  SIMON BOLIVAR', 73, 'CALLE 1 OESTE NO 42 A 94', '73/02', 19, 'URBANO\r'),
(272, '73/03  ANTONIA SANTOS', 73, 'CRA 38C OESTE # 3A-00', '73/03', 19, 'URBANO\r'),
(273, '74/01 IE MULTIPROPOSITO', 74, 'CRA. 56 NO. 7 OESTE - 190', '74/01', 20, 'URBANO\r'),
(274, '74/02 JORGE ELIESER GONZALES RUBIO', 74, 'CALLE 8 OESTE NO. 52 - 16', '74/02', 20, 'URBANO\r'),
(275, '74/03 REPUBLICA DE PANAMA', 74, 'DIAG 48 NO. 12 - 00 OESTE', '74/03', 20, 'URBANO\r'),
(276, '74/04 SANTA LUISA', 74, 'CALLE CENTRAL VDA. LA SIRENA', '74/04', 20, 'URBANO\r'),
(277, '74/05 LUIS ALBERTO ROSALES', 74, 'CRA 51B NO. 6H - 00 OESTE', '74/05', 20, 'URBANO\r'),
(278, '75/01 IE TECNICA CIUDADELA DESEPAZ', 75, 'CARRERA 23 NO 1206- 16', '75/01', 21, 'URBANO\r'),
(279, '75/02 NUEVO AMANECER', 75, 'CL 123 28D4 - 54', '75/02', 21, 'URBANO\r'),
(280, '75/03 PROGRESANDO JUNTOS', 75, 'KR 82 24 F 30', '75/03', 21, 'URBANO\r'),
(281, '76/01 IE NAVARRO -  JUAN BAUTISTA DE LA SALLE', 76, 'Corregimiento Navarro-', '76/01', 51, 'RURAL\r'),
(282, '76/02 JUAN DEL CORRAL', 76, 'Vrda.El Estero cgto Navarro', '76/02', 51, 'RURAL\r'),
(283, '77/01 IE HORMIGUERO  -  PANTANO DE VARGAS', 77, 'CRA. 143 CALLEJ CASCAJAL vereda cascajal', '77/01', 52, 'RURAL\r'),
(284, '77/02 ANTONIO VILLAVICENCIO', 77, 'Cgto.Hormiguero-', '77/02', 52, 'RURAL\r'),
(285, '77/03 TULIA BORRERO MERCADO', 77, 'Vrda.Morgan .Cgto.Navarro', '77/03', 52, 'RURAL\r'),
(286, '77/04 HOGAR JUVENIL EL HORMIGUERO', 77, 'Vereda Cascajal', '77/04', 52, 'RURAL\r'),
(287, '78/01 IE TECNICA DE BALLET CLASICO INCOLBALLET', 78, 'KM 4 VIA JAMUNDI', '78/01', 51, 'RURAL\r'),
(288, '78/02 CAÑASGORDAS', 78, 'CRA 102 21-81', '78/02', 51, 'RURAL\r'),
(289, '79/01 IE PANCE ', 79, 'Cgto Pance La Voragine KM1', '79/01', 53, 'RURAL\r'),
(290, '79/02 REPUBLICA DE SANTO DOMINGO', 79, 'Cgto.Pance Cabecera', '79/02', 53, 'RURAL\r'),
(291, '79/03 PIO XII', 79, 'Vereda La Voragine', '79/03', 53, 'RURAL\r'),
(292, '79/04 SAN FRANCISCO', 79, 'Vrda. San francisco Cgto Pance', '79/04', 53, 'RURAL\r'),
(293, '79/05 LAUREANO GOMEZ', 79, 'Vrda.El Banqueo cgto Pance', '79/05', 53, 'RURAL\r'),
(294, '80/01 IE LA BUITRERA JOSE MARIA GARCIA DE TOLEDO', 80, 'CGTO LA BUITRERA KM 3cabecera', '80/01', 54, 'RURAL\r'),
(295, '80/02 LOS COMUNEROS', 80, 'Vrda.Alto del Rosario-La buitrera.', '80/02', 54, 'RURAL\r'),
(296, '80/03 SOLEDAD ACOSTA DE SAMPER', 80, 'Vrda el Otoño-La buitrera', '80/03', 54, 'RURAL\r'),
(297, '80/04 NUESTRA SENORA DE LAS LAJAS', 80, 'CGTO LA BUITRERA Parte media KM 6', '80/04', 54, 'RURAL\r'),
(298, '80/05 SAN GABRIEL ', 80, 'Km 4, Callejon polvorines', '80/05', 18, 'URBANO\r'),
(299, '81/01 IE VILLACARMELO -CACIQUE CALARCA', 81, 'VEREDA LA FONDA Cgto Villacarmelo', '81/01', 55, 'RURAL\r'),
(300, '81/02 NUESTRA SENORA DEL CARMEN', 81, 'Cgto. Villacarmelo-Cabecera', '81/02', 55, 'RURAL\r'),
(301, '82/01 IE LOS ANDES -  TIERRA DE HOMBRES', 82, 'CORREG. LOS ANDES  vda. Cabuyal', '82/01', 56, 'RURAL\r'),
(302, '82/02 JUAN PABLO I ', 82, 'CORREG. LOS ANDES - VEREDA LOS KARPATOS', '82/02', 56, 'RURAL\r'),
(303, '82/03 FRANCISCO JOSE DE CALDAS', 82, 'CORREG. LOS ANDES', '82/03', 56, 'RURAL\r'),
(304, '83/01  IE PICHINDE - JOSE HOLGUIN GARCES ', 83, 'GOLONDRINAS CABECERA', '83/01', 57, 'RURAL\r'),
(305, '83/02 LA INMACULADA CONCEPCION', 83, 'CORREG. PICHINDE', '83/02', 57, 'RURAL\r'),
(306, '83/03 SERGIO CANTILLO ', 83, 'CORRREGIMIENTO PICHINDE', '83/03', 57, 'RURAL\r'),
(307, '84/01 IE FELIDIA - JOSE HOLGUIN GARCES ', 84, 'CTO FELIDIA CABECERA', '84/01', 59, 'RURAL\r'),
(308, '84/02  REPUBLICA DE CUBA', 84, 'CORREGIMIENTO FELIDIA  ()', '84/02', 59, 'RURAL\r'),
(309, '84/03 CRISTOBAL COLON - BARRIO CTO FELIDIA', 84, 'CORREGIMIENTO FELIDIA VEREDA EL DIAMANTE', '84/03', 59, 'RURAL\r'),
(310, '85/01 IE LA LEONERA ITA FARALLONES', 85, 'CGTO LEONERA', '85/01', 58, 'RURAL\r'),
(311, '85/02 JORGE ELIECER GAITAN - BARRIO VEREDA EL PORVENIR', 85, 'VEREDA EL PORVENIR CGTO LA LEONERA', '85/02', 58, 'RURAL\r'),
(312, '85/03 JUAN DE LOS BARRIOS', 85, 'VEREDA PAJUY - LA LEONERA', '85/03', 58, 'RURAL\r'),
(313, '86/01 IE SALADITO - FCO JOSE LLOREDA MERA ', 86, 'CORREGIMIENTO EL SALADITO -', '86/01', 60, 'RURAL\r'),
(314, '86/02  LUIS FERNANDO LLOREDA ZAMORANO', 86, 'CORREG. SALADITO', '86/02', 60, 'RURAL\r'),
(315, '86/03  FRANCISCO MIRANDA', 86, 'KIL. 18 VIA AL MAR CGTO SALADITO', '86/03', 60, 'RURAL\r'),
(316, '86/04  BOYACA -  CTO LA ELVIRA', 86, 'CORREGIMIENTO LA ELVIRA SALADITO', '86/04', 60, 'RURAL\r'),
(317, '86/05 IGNACIO HERRERA Y VERGARA', 86, 'CORREG. LA ELVIRA ( VDA ALTO AGUACATAL)', '86/05', 60, 'RURAL\r'),
(318, '86/06 NUEVA SAN FRANCISCO', 86, 'VEREDA LOS LAURELES', '86/06', 60, 'RURAL\r'),
(319, '87/01 IE LA PAZ- SAAVEDRA GALINDO', 87, 'CGTO LA PAZ, VEREDA VILLA DEL ROSARIO', '87/01', 62, 'RURAL\r'),
(320, '87/02 SAGRADO CORAZON', 87, 'CGTO LA CASTILLA la paz', '87/02', 62, 'RURAL\r'),
(321, '87/03 LA GRANJA', 87, 'CORREGIMIENTO LA PAZ', '87/03', 62, 'RURAL\r'),
(322, '87/04 JORGE ROBLEDO', 87, 'CGTO LA PAZ', '87/04', 62, 'RURAL\r'),
(323, '87/05 VILLA DEL ROSARIO', 87, 'CGTO LA PAZ, VEREDA VILLA DEL ROSARIO', '87/05', 62, 'RURAL\r'),
(324, '88/01 IE MONTEBELLO', 88, 'CGTO MONTEBELLO CABECERA', '88/01', 64, 'RURAL\r'),
(325, '88/02 SAN PEDRO APOSTOL', 88, 'CGTO MONTEBELLO CABECERA', '88/02', 64, 'RURAL\r'),
(326, '88/03 ANDRES JOAQUIN LENIS', 88, 'CGTO MONTEBELLO VEREDA CAMPO ALEGRE', '88/03', 64, 'RURAL\r'),
(327, '89/01 IE ALFONSO LOPEZ PUMAREJO', 89, 'CARRERA 7S BIS CALLE 72 Y 73', '89/01', 7, 'URBANO\r'),
(328, '89/02 RAFAEL POMBO', 89, 'CRA 7 R BIS NO. 72 - 124', '89/02', 7, 'URBANO\r'),
(329, '89/03 PURIFICACION TRUJILLO', 89, 'CRA 7 J BIS CALLE 72 Y 73 ESQUINA', '89/03', 7, 'URBANO\r'),
(330, '89/04 LOS FARALLONES', 89, 'CRA 7J BIS NO. 72 - 00', '89/04', 7, 'URBANO\r'),
(331, '89/05 CENTRAL PROVIVIENDA', 89, 'CALLE 72A NO. 7C BIS - 10', '89/05', 7, 'URBANO\r'),
(332, '90/01 IE GOLONDRINAS', 90, 'GOLONDRINAS CABECERA', '90/01', 65, 'RURAL\r'),
(333, '90/02 ANTONIO BARBERENA', 90, 'GOLONDRINAS CABECERA', '90/02', 65, 'RURAL\r'),
(334, '91/01 IE  NUEVO LATIR', 91, 'Calle 76 No. 28- 20', '91/01', 15, 'URBANO\r'),
(335, '91/02 CIUDADELA EDUCATIVA ISAIAS DUARTE CANCINO', 91, 'CALLE 96 CARRERA 28', '91/02', 15, 'URBANO\r'),
(336, '92/01 IE  GENERAL JOSE MARIA CABAL ', 92, 'Cl. 2c Oe. NO. 83-30', '92/01', 18, 'URBANO\r'),
(337, 'ASODISVALLE - SEDE PRINCIPAL', 93, 'Dg 71A1# 26I - 68', 'N/A', 13, 'URBANO\r'),
(338, 'TODAS LAS SEDES FOCALIZADAS', 94, 'N/A', 'N/A', 0, 'N/A'),
(339, 'TODAS LAS SEDES FOCALIZADAS', 95, 'N/A', 'N/A', 0, 'N/A'),
(340, 'TODA LAS SEDES FOCALIZADAS', 96, 'N/A', 'N/A', 0, 'N/A'),
(341, 'TODAS LAS SEDES FOCALIZADAS', 97, 'N/A', 'N/A', 0, 'N/A'),
(342, '20/04 ANA MARIA VERNAZA', 20, 'CALLE 72 # 8B - 32, COMUNA 7', '20/04', 7, 'URBANO ');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `temperaturas`
--

CREATE TABLE `temperaturas` (
  `id_temperatura` int(11) NOT NULL,
  `id_visita_tecnica` int(11) NOT NULL,
  `componente` varchar(255) NOT NULL,
  `temperatura` int(11) DEFAULT NULL,
  `concepto` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tiporacion`
--

CREATE TABLE `tiporacion` (
  `id_tipo_racion` int(11) NOT NULL,
  `descripcion` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tiporacion`
--

INSERT INTO `tiporacion` (`id_tipo_racion`, `descripcion`) VALUES
(1, 'Industrializado'),
(4, 'Jornada Unica'),
(2, 'Preparado en sitio AM'),
(3, 'Preparado en sitio PM');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `toma_peso`
--

CREATE TABLE `toma_peso` (
  `id_toma_peso` int(11) NOT NULL,
  `id_visita_tecnica` int(11) NOT NULL,
  `desperdicio` enum('Si','No') NOT NULL,
  `menu_del_dia` varchar(255) NOT NULL,
  `nivel1` decimal(10,2) NOT NULL,
  `nivel2` decimal(10,2) NOT NULL,
  `nivel3` decimal(10,2) NOT NULL,
  `nivel4` decimal(10,2) NOT NULL,
  `nivel5` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `observacion` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `correo` varchar(255) NOT NULL,
  `correo_corto` varchar(225) NOT NULL,
  `contrasena` varchar(255) DEFAULT NULL,
  `rol` enum('operador','supervisor','nutricionista','administrador') NOT NULL,
  `id_operador` int(11) DEFAULT NULL,
  `fecha_ingreso` timestamp NOT NULL DEFAULT current_timestamp(),
  `habilitar_acceso` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `correo`, `correo_corto`, `contrasena`, `rol`, `id_operador`, `fecha_ingreso`, `habilitar_acceso`) VALUES
(0, 'Ana Carolina Aguado', 'ana.carolina@cali.edu.co', '', '$2b$12$HgMz7iQox2GZd2V6KPhfluRMaMVuIZ0yN.adKtO6wsXpdSNsfnomO', 'nutricionista', NULL, '2025-02-04 20:58:06', 1),
(21, 'Daniel Torres', 'daniel.torres@cali.edu.co', 'daniel.torres', '$2b$12$D.4xGi4uKhkRXCMdcq9c1eMxY3ijwNwkoHwGyBfQ0GC5vekALSbKm', 'supervisor', NULL, '2024-11-12 11:41:08', 1),
(28, 'Melisa Ruiz', 'melisa.ruiz@cali.edu.co', 'melisa.ruiz', '$2b$12$Pe9HCc4/LrpMID2haGRBQu/ztYhMMHYXDMsA1huyeI3xm/beK02VC', 'supervisor', NULL, '2024-11-12 11:41:08', 1),
(29, 'Gabriela Giraldo', 'Gabriela.giraldo@cali.edu.co', 'Gabriela.giraldo', '$2b$12$dj9iljsR89uUwE5s0xn9TOXvN5jDaID8PN3zf4TmdtK9kQlvJTJ.W', 'nutricionista', NULL, '2024-11-12 11:41:08', 1),
(30, 'Sofia Melendez', 'sofia.melendez@cali.edu.co', 'sofia.melendez', '$2b$12$h1wjLO6BphUwzhuWQRAsCOQGb9L5h55EdR5NghjeHA00/8/3Uqi.y', 'nutricionista', NULL, '2024-11-12 11:41:08', 1),
(31, 'Claudia Lorena Castaño', 'claudia.castano@cali.edu.co', 'claudia.castano', '$2b$12$lbOaIKzd9ARgJG.qy9DOLO3jrpG0kC7cPj2mdFfZ4PL5G.QlVf2d.', 'supervisor', NULL, '2024-11-12 11:41:08', 1),
(32, 'Ana Isabel Popo', 'ana.popo@cali.edu.co', 'ana.popo', '$2b$12$UMFahFUUNeRe07eoO2.zdehFbco3BoPSX/nenIKGDaz0GWhCmyOA6', 'supervisor', NULL, '2024-11-12 11:41:08', 1),
(33, 'Maria Fernanda Oliveros ', 'maria.oliveros@cali.edu.co', 'maria.oliveros', '$2b$12$01jwba/Hn8U.hzuSDt0fM.4tuLCB5DzRR41rHsUanQlokQyf3tQeC', 'supervisor', NULL, '2024-11-12 11:41:08', 1),
(34, 'Yudy Garcia', 'yudy.garcia@cali.edu.co', 'yudy.garcia', '$2b$12$tdhaGiv1pfcYqLWw4k652u8bldUzwjHQ5osEoho5pzoVMi1QEMsa.', 'supervisor', NULL, '2024-11-12 11:41:08', 1),
(35, 'Leidy Garcia', 'leidy.garcia@cali.edu.co', 'leidy.garcia', '$2b$12$XduYk/j2HGVsbQTaJD6OUuK1FTutgurDswXbMizTE4XOkoFgd8Uii', 'supervisor', NULL, '2024-11-12 11:41:08', 1),
(36, 'Felipe Guzman', 'felipe.guzman@cali.edu.co', 'felipe.guzman', '$2b$12$iu63T/nUuWiTXKdOPq8zpeZLDF2FKqxpDBpQSgty7rGLuBGLoRQca', 'supervisor', NULL, '2024-11-12 11:41:08', 1),
(37, 'Maria Eugenia Arias ', 'maria.arias@cali.edu.co', 'maria.arias', '$2b$12$k1tI8GowcVp8VDxmBms6IO9fXt3evLeB5s8lUBoufB/wxDRszXZ4C', 'supervisor', NULL, '2024-11-12 11:41:08', 1),
(38, 'Sebastian Giraldo', 'sgiraldo@cali.gov.co', 'sgiraldo', '$2b$12$PCX0e5GQ5DtBdOqh5ekwJOeVchyn3Ed3kiGT9Uyzc8S9NeWb39M7W', 'supervisor', NULL, '2024-11-12 11:41:08', 1),
(46, 'JOHAN STEVEN ROJAS SOLIS', 'johan.rojas@cali.edu.co', 'johan.rojas', '$2b$12$6wdtZrthX9PtaueBU.TUOePd5.I/JJxWhgiaVnbe1c2It3/FSVya2', 'nutricionista', NULL, '2024-11-12 11:41:08', 1),
(55, 'Componente Técnico Nutricional del PAE', 'componente.nutricional@cali.edu.co', 'componentes.nutricional', '$2b$12$GSa/gxS5YCvBIoi/CRPtG.jl/Ucaz4w8ZeJLo.KBl71j8DLrZWqzC', 'nutricionista', NULL, '2024-11-19 02:45:28', 1),
(61, 'Daniel Quintero J.', 'daniel.quintero@cali.edu.co', 'daniel.quintero', '$2b$12$asZnR2AvtMf.eTxTUVcGq.V/nutFJwsHhV.CtLmWGAg4TJhpn/cl.', 'administrador', NULL, '2024-11-20 22:46:31', 1),
(62, 'Admin Nutricionista', 'dk30jim19@gmail.com', 'dk30jim19', '$2b$12$liRksPA3pSp02MGZZWoG7OPVn1bEvjgowscPeR5z7y89MhxCbgq0W', 'nutricionista', NULL, '2024-11-21 05:07:13', 1),
(66, 'Construyendo', 'coordinadora.programapae@nrc.com.co', 'coordinadora.programapae', '$2b$12$tGtom3JI85H2eZUGGQs2xeSL9O04/sSrMdKfDHnc2fXNuBFF7D2e.', 'operador', 1, '2024-11-22 07:48:55', 1),
(67, 'Valle Solidario', 'nutricion@vallesolidario.com', 'nutricion', '$2b$12$pm7SLf4qkRWXXlCsZv.qce1CEc4pYKa3xBOC/rIuJ20dnTtrVI54C', 'operador', 3, '2024-11-22 07:51:46', 1),
(71, 'Nutriendo', 'coor.operativocali@fomento.com.co', 'coor.operativocali', '$2b$12$eLvU5b6TzcsUy.RgB8uQV./bwMg1HwsV1k1i1maH/RrgTSvRlMHqi', 'operador', 4, '2024-11-22 07:56:26', 1),
(72, 'Nutriendo 2', 'coor.operativocali2@fomento.com.co', 'coor.operativocali2', '$2b$12$LHgL3DSW5tNQjX5rQqd/DO0DObkgsUFqmnY2oaV1CNL9BSxz.MpRe', 'operador', 4, '2024-11-22 07:57:32', 1),
(73, 'Accion por Colombia', 'proyectocali@accionporcolombia.com', 'proyectocali', '$2b$12$jN.WL8XyzKhuSLWeeK2Ghur/EUO94buYX9aBEDPlEqPMrQ.BDvIAe', 'operador', 2, '2024-11-22 07:58:02', 1),
(84, 'Fran Anibal Mesias', 'fran.mesias@cali.gov.co', 'fran.mesias', '$2b$12$joH.5XnZ8ALIeXBy7WMNTeQHCQGi0NhkkCtWL92m6eiXlblTF2JrW', 'administrador', NULL, '2024-11-23 07:03:43', 1),
(86, 'Daniel Quintero', 'qdanif@gmail.com', '', '$2b$12$nH5NnL.iVgQ4dG.YWNlyxenqKoLYIPlbdlBBCbgkSHczNkWfRLQpu', 'operador', 1, '2024-12-21 06:04:25', 1),
(87, 'Supervisor Daniel', 'dan30jim19@gmail.com', '', '$2b$12$NdyVeZ3tNAZ8.NfhWxJmlOAjUS2z/WO1FuZPZSo5c/7Ruh51uUXY6', 'supervisor', NULL, '2024-12-26 14:14:26', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `verificacion_menu`
--

CREATE TABLE `verificacion_menu` (
  `id` int(11) NOT NULL,
  `fecha_visita` date NOT NULL,
  `hora_visita` time DEFAULT NULL,
  `zona` varchar(50) DEFAULT NULL,
  `jornada` varchar(50) DEFAULT NULL,
  `contrato` varchar(50) DEFAULT NULL,
  `id_operador` int(11) NOT NULL,
  `institucion_id` int(11) NOT NULL,
  `sede_id` int(11) DEFAULT NULL,
  `tipo_racion_id` int(11) NOT NULL,
  `numero_menu_oficial` int(11) DEFAULT NULL,
  `numero_menu_intercambio` int(11) DEFAULT NULL,
  `nivel_1` int(11) DEFAULT 0,
  `nivel_2` int(11) DEFAULT 0,
  `nivel_3` int(11) DEFAULT 0,
  `nivel_4` int(11) DEFAULT 0,
  `nivel_5` int(11) DEFAULT 0,
  `total` int(11) GENERATED ALWAYS AS (`nivel_1` + `nivel_2` + `nivel_3` + `nivel_4` + `nivel_5`) STORED,
  `observacion_general` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `hallazgo` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `verificacion_menu_detalles`
--

CREATE TABLE `verificacion_menu_detalles` (
  `id` int(11) NOT NULL,
  `verificacion_menu_id` int(11) NOT NULL,
  `componentes` varchar(255) NOT NULL,
  `valor_cumplimiento` int(11) DEFAULT NULL,
  `menu_oficial` text DEFAULT NULL,
  `menu_intercambio` text DEFAULT NULL,
  `propiedades_organolepticas` tinyint(1) DEFAULT NULL CHECK (`propiedades_organolepticas` in (0,1,2)),
  `observacion` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `fecha_vencimiento` date DEFAULT NULL,
  `lote` varchar(50) DEFAULT NULL,
  `peso_nivel_escolar_1` int(11) DEFAULT NULL,
  `peso_nivel_escolar_2` int(11) DEFAULT NULL,
  `peso_nivel_escolar_3` int(11) DEFAULT NULL,
  `peso_nivel_escolar_4` int(11) DEFAULT NULL,
  `peso_nivel_escolar_5` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `visitas_bodega`
--

CREATE TABLE `visitas_bodega` (
  `id_visita` int(11) NOT NULL,
  `operador` int(11) NOT NULL,
  `tipo_visita` enum('Visita Inicio','Visita Seguimiento','Visita Cierre') NOT NULL,
  `fecha_visita` date NOT NULL,
  `numero_visita` int(11) DEFAULT NULL,
  `observacion_general` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `visita_tecnica`
--

CREATE TABLE `visita_tecnica` (
  `id_visita_tecnica` int(11) NOT NULL,
  `fecha_visita` date NOT NULL,
  `hora_visita` time NOT NULL,
  `operador` int(11) NOT NULL,
  `institucion_id` int(11) NOT NULL,
  `sede_id` int(11) NOT NULL,
  `codigo_sede` varchar(50) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `zona` varchar(50) DEFAULT NULL,
  `focalizacion` int(11) NOT NULL,
  `tipo_racion_tecnica` varchar(50) NOT NULL,
  `observacion_general` varchar(5000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `archivos`
--
ALTER TABLE `archivos`
  ADD PRIMARY KEY (`id_archivo`),
  ADD KEY `archivos_ibfk_1` (`id_intercambio`);

--
-- Indices de la tabla `archivos_verificacion`
--
ALTER TABLE `archivos_verificacion`
  ADD PRIMARY KEY (`id_archivos_verificacion`),
  ADD KEY `verificacion_id` (`verificacion_id`);

--
-- Indices de la tabla `archivos_visita_tecnica`
--
ALTER TABLE `archivos_visita_tecnica`
  ADD PRIMARY KEY (`id_archivo_tecnica`),
  ADD KEY `visita_tecnica_id` (`visita_tecnica_id`);

--
-- Indices de la tabla `componente_alimentario_1`
--
ALTER TABLE `componente_alimentario_1`
  ADD PRIMARY KEY (`id_componente_alimentario`),
  ADD KEY `visita_id` (`id_visita_tecnica`);

--
-- Indices de la tabla `componente_alimentario_promedio`
--
ALTER TABLE `componente_alimentario_promedio`
  ADD PRIMARY KEY (`id_promedio`),
  ADD KEY `id_visita_tecnica` (`id_visita_tecnica`);

--
-- Indices de la tabla `detalles_menu`
--
ALTER TABLE `detalles_menu`
  ADD PRIMARY KEY (`id_detalle_menu`),
  ADD KEY `id_tipo_racion` (`id_tipo_racion`),
  ADD KEY `fk_detalle_menu_intercambio` (`id_intercambio`);

--
-- Indices de la tabla `dotacion_menaje`
--
ALTER TABLE `dotacion_menaje`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_infraestructura` (`id_infraestructura`);

--
-- Indices de la tabla `firmas`
--
ALTER TABLE `firmas`
  ADD PRIMARY KEY (`id_firma`),
  ADD KEY `id_intercambio` (`id_intercambio`);

--
-- Indices de la tabla `firmas_bodega`
--
ALTER TABLE `firmas_bodega`
  ADD PRIMARY KEY (`id_firma_bodega`),
  ADD KEY `fk_id_visita` (`id_visita`);

--
-- Indices de la tabla `firmas_infraestructura`
--
ALTER TABLE `firmas_infraestructura`
  ADD PRIMARY KEY (`id_firma`),
  ADD KEY `id_infraestructura` (`id_infraestructura`);

--
-- Indices de la tabla `firmas_nutricionistas`
--
ALTER TABLE `firmas_nutricionistas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `firmas_tecnica`
--
ALTER TABLE `firmas_tecnica`
  ADD PRIMARY KEY (`id_firma`),
  ADD KEY `id_visita_tecnica` (`id_visita_tecnica`);

--
-- Indices de la tabla `firmas_verificacion`
--
ALTER TABLE `firmas_verificacion`
  ADD PRIMARY KEY (`id_firma_verificacion`),
  ADD KEY `id_verificacion` (`id_verificacion`);

--
-- Indices de la tabla `fotos_bodega`
--
ALTER TABLE `fotos_bodega`
  ADD PRIMARY KEY (`id_foto`),
  ADD KEY `id_visita` (`id_visita`);

--
-- Indices de la tabla `historial_cambios`
--
ALTER TABLE `historial_cambios`
  ADD PRIMARY KEY (`id_historia_cambios`);

--
-- Indices de la tabla `industrializado`
--
ALTER TABLE `industrializado`
  ADD PRIMARY KEY (`id_industrializado`),
  ADD KEY `id_tipo_racion` (`id_tipo_racion`);

--
-- Indices de la tabla `infraestructura`
--
ALTER TABLE `infraestructura`
  ADD PRIMARY KEY (`id_infraestructura`),
  ADD KEY `fk_infraestructura_operador` (`operador`),
  ADD KEY `fk_infraestructura_institucion` (`institucion`),
  ADD KEY `fk_infraestructura_sede` (`sede`);

--
-- Indices de la tabla `instituciones`
--
ALTER TABLE `instituciones`
  ADD PRIMARY KEY (`id_institucion`),
  ADD KEY `fk_id_operador` (`id_operador`);

--
-- Indices de la tabla `instituciones_sedes`
--
ALTER TABLE `instituciones_sedes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_institucion` (`id_institucion`),
  ADD KEY `id_sede` (`id_sede`),
  ADD KEY `fk_institucion_sedes_intercambio` (`id_intercambio`);

--
-- Indices de la tabla `intercambios`
--
ALTER TABLE `intercambios`
  ADD PRIMARY KEY (`id_intercambio`),
  ADD KEY `id_operador` (`id_operador`),
  ADD KEY `id_tipo_racion` (`id_tipo_racion`);

--
-- Indices de la tabla `jornadaunica`
--
ALTER TABLE `jornadaunica`
  ADD PRIMARY KEY (`id_jornada_unica`),
  ADD KEY `id_tipo_racion` (`id_tipo_racion`);

--
-- Indices de la tabla `operadores`
--
ALTER TABLE `operadores`
  ADD PRIMARY KEY (`id_operador`),
  ADD UNIQUE KEY `nombre` (`nombre`),
  ADD KEY `idx_nombre` (`nombre`);

--
-- Indices de la tabla `preguntas_bodega`
--
ALTER TABLE `preguntas_bodega`
  ADD PRIMARY KEY (`id_pregunta`);

--
-- Indices de la tabla `preguntas_infraestructura`
--
ALTER TABLE `preguntas_infraestructura`
  ADD PRIMARY KEY (`id_pregunta`);

--
-- Indices de la tabla `preguntas_tecnica`
--
ALTER TABLE `preguntas_tecnica`
  ADD PRIMARY KEY (`id_tecnica`);

--
-- Indices de la tabla `preparadoensitioam`
--
ALTER TABLE `preparadoensitioam`
  ADD PRIMARY KEY (`id_preparado_sitio_am`),
  ADD KEY `fk_tipo_racion` (`id_tipo_racion`);

--
-- Indices de la tabla `preparadoensitiopm`
--
ALTER TABLE `preparadoensitiopm`
  ADD PRIMARY KEY (`id_preparado_sitio_pm`),
  ADD KEY `id_tipo_racion` (`id_tipo_racion`);

--
-- Indices de la tabla `puntaje_cumplimiento`
--
ALTER TABLE `puntaje_cumplimiento`
  ADD PRIMARY KEY (`id_puntaje`),
  ADD KEY `verificacion_menu_id` (`verificacion_menu_id`);

--
-- Indices de la tabla `respuestas_bodega`
--
ALTER TABLE `respuestas_bodega`
  ADD PRIMARY KEY (`id_respuesta`),
  ADD KEY `id_visita` (`id_visita`),
  ADD KEY `id_pregunta` (`id_pregunta`);

--
-- Indices de la tabla `respuestas_infraestructura`
--
ALTER TABLE `respuestas_infraestructura`
  ADD PRIMARY KEY (`id_respuesta`),
  ADD KEY `id_infraestructura` (`id_infraestructura`),
  ADD KEY `respuestas_ibfk_1` (`id_pregunta`);

--
-- Indices de la tabla `respuestas_tecnica`
--
ALTER TABLE `respuestas_tecnica`
  ADD PRIMARY KEY (`id_respuesta`),
  ADD KEY `visita_tecnica_id` (`visita_tecnica_id`),
  ADD KEY `pregunta_id` (`pregunta_id`);

--
-- Indices de la tabla `sedes`
--
ALTER TABLE `sedes`
  ADD PRIMARY KEY (`id_sede`),
  ADD KEY `fk_id_institucion` (`id_institucion`);

--
-- Indices de la tabla `temperaturas`
--
ALTER TABLE `temperaturas`
  ADD PRIMARY KEY (`id_temperatura`),
  ADD KEY `id_visita_tecnica` (`id_visita_tecnica`);

--
-- Indices de la tabla `tiporacion`
--
ALTER TABLE `tiporacion`
  ADD PRIMARY KEY (`id_tipo_racion`),
  ADD KEY `idx_descripcion` (`descripcion`);

--
-- Indices de la tabla `toma_peso`
--
ALTER TABLE `toma_peso`
  ADD PRIMARY KEY (`id_toma_peso`),
  ADD KEY `id_visita_tecnica` (`id_visita_tecnica`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD KEY `id_operador` (`id_operador`);

--
-- Indices de la tabla `verificacion_menu`
--
ALTER TABLE `verificacion_menu`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_verificacion_menu_operador` (`id_operador`),
  ADD KEY `fk_verificacion_menu_institucion` (`institucion_id`),
  ADD KEY `fk_verificacion_menu_sede` (`sede_id`),
  ADD KEY `fk_verificacion_menu_tipo_racion` (`tipo_racion_id`);

--
-- Indices de la tabla `verificacion_menu_detalles`
--
ALTER TABLE `verificacion_menu_detalles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `verificacion_menu_detalles_ibfk_1` (`verificacion_menu_id`);

--
-- Indices de la tabla `visitas_bodega`
--
ALTER TABLE `visitas_bodega`
  ADD PRIMARY KEY (`id_visita`),
  ADD KEY `operador` (`operador`);

--
-- Indices de la tabla `visita_tecnica`
--
ALTER TABLE `visita_tecnica`
  ADD PRIMARY KEY (`id_visita_tecnica`),
  ADD KEY `institucion_id` (`institucion_id`),
  ADD KEY `sede_id` (`sede_id`),
  ADD KEY `fk_visita_tecnica_operador` (`operador`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `archivos`
--
ALTER TABLE `archivos`
  MODIFY `id_archivo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=76;

--
-- AUTO_INCREMENT de la tabla `archivos_verificacion`
--
ALTER TABLE `archivos_verificacion`
  MODIFY `id_archivos_verificacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `archivos_visita_tecnica`
--
ALTER TABLE `archivos_visita_tecnica`
  MODIFY `id_archivo_tecnica` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `componente_alimentario_1`
--
ALTER TABLE `componente_alimentario_1`
  MODIFY `id_componente_alimentario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=681;

--
-- AUTO_INCREMENT de la tabla `componente_alimentario_promedio`
--
ALTER TABLE `componente_alimentario_promedio`
  MODIFY `id_promedio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=71;

--
-- AUTO_INCREMENT de la tabla `detalles_menu`
--
ALTER TABLE `detalles_menu`
  MODIFY `id_detalle_menu` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=82;

--
-- AUTO_INCREMENT de la tabla `dotacion_menaje`
--
ALTER TABLE `dotacion_menaje`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=816;

--
-- AUTO_INCREMENT de la tabla `firmas`
--
ALTER TABLE `firmas`
  MODIFY `id_firma` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=79;

--
-- AUTO_INCREMENT de la tabla `firmas_bodega`
--
ALTER TABLE `firmas_bodega`
  MODIFY `id_firma_bodega` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `firmas_infraestructura`
--
ALTER TABLE `firmas_infraestructura`
  MODIFY `id_firma` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `firmas_nutricionistas`
--
ALTER TABLE `firmas_nutricionistas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `firmas_tecnica`
--
ALTER TABLE `firmas_tecnica`
  MODIFY `id_firma` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `firmas_verificacion`
--
ALTER TABLE `firmas_verificacion`
  MODIFY `id_firma_verificacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT de la tabla `fotos_bodega`
--
ALTER TABLE `fotos_bodega`
  MODIFY `id_foto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `historial_cambios`
--
ALTER TABLE `historial_cambios`
  MODIFY `id_historia_cambios` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `infraestructura`
--
ALTER TABLE `infraestructura`
  MODIFY `id_infraestructura` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `instituciones_sedes`
--
ALTER TABLE `instituciones_sedes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=227;

--
-- AUTO_INCREMENT de la tabla `intercambios`
--
ALTER TABLE `intercambios`
  MODIFY `id_intercambio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT de la tabla `operadores`
--
ALTER TABLE `operadores`
  MODIFY `id_operador` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `preguntas_tecnica`
--
ALTER TABLE `preguntas_tecnica`
  MODIFY `id_tecnica` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=237;

--
-- AUTO_INCREMENT de la tabla `puntaje_cumplimiento`
--
ALTER TABLE `puntaje_cumplimiento`
  MODIFY `id_puntaje` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT de la tabla `respuestas_bodega`
--
ALTER TABLE `respuestas_bodega`
  MODIFY `id_respuesta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3472;

--
-- AUTO_INCREMENT de la tabla `respuestas_infraestructura`
--
ALTER TABLE `respuestas_infraestructura`
  MODIFY `id_respuesta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3106;

--
-- AUTO_INCREMENT de la tabla `respuestas_tecnica`
--
ALTER TABLE `respuestas_tecnica`
  MODIFY `id_respuesta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2597;

--
-- AUTO_INCREMENT de la tabla `temperaturas`
--
ALTER TABLE `temperaturas`
  MODIFY `id_temperatura` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de la tabla `toma_peso`
--
ALTER TABLE `toma_peso`
  MODIFY `id_toma_peso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `verificacion_menu`
--
ALTER TABLE `verificacion_menu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `verificacion_menu_detalles`
--
ALTER TABLE `verificacion_menu_detalles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=223;

--
-- AUTO_INCREMENT de la tabla `visitas_bodega`
--
ALTER TABLE `visitas_bodega`
  MODIFY `id_visita` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `visita_tecnica`
--
ALTER TABLE `visita_tecnica`
  MODIFY `id_visita_tecnica` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `archivos`
--
ALTER TABLE `archivos`
  ADD CONSTRAINT `archivos_ibfk_1` FOREIGN KEY (`id_intercambio`) REFERENCES `intercambios` (`id_intercambio`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_archivos_intercambio` FOREIGN KEY (`id_intercambio`) REFERENCES `intercambios` (`id_intercambio`) ON DELETE CASCADE;

--
-- Filtros para la tabla `archivos_verificacion`
--
ALTER TABLE `archivos_verificacion`
  ADD CONSTRAINT `archivos_verificacion_ibfk_1` FOREIGN KEY (`verificacion_id`) REFERENCES `verificacion_menu` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `archivos_visita_tecnica`
--
ALTER TABLE `archivos_visita_tecnica`
  ADD CONSTRAINT `archivos_visita_tecnica_ibfk_1` FOREIGN KEY (`visita_tecnica_id`) REFERENCES `visita_tecnica` (`id_visita_tecnica`) ON DELETE CASCADE;

--
-- Filtros para la tabla `componente_alimentario_1`
--
ALTER TABLE `componente_alimentario_1`
  ADD CONSTRAINT `fk_componente_alimentario_1_visita_tecnica` FOREIGN KEY (`id_visita_tecnica`) REFERENCES `visita_tecnica` (`id_visita_tecnica`) ON DELETE CASCADE;

--
-- Filtros para la tabla `componente_alimentario_promedio`
--
ALTER TABLE `componente_alimentario_promedio`
  ADD CONSTRAINT `fk_componente_alimentario_promedio_visita_tecnica` FOREIGN KEY (`id_visita_tecnica`) REFERENCES `visita_tecnica` (`id_visita_tecnica`) ON DELETE CASCADE;

--
-- Filtros para la tabla `detalles_menu`
--
ALTER TABLE `detalles_menu`
  ADD CONSTRAINT `detalles_menu_ibfk_1` FOREIGN KEY (`id_intercambio`) REFERENCES `intercambios` (`id_intercambio`) ON DELETE CASCADE,
  ADD CONSTRAINT `detalles_menu_ibfk_2` FOREIGN KEY (`id_tipo_racion`) REFERENCES `tiporacion` (`id_tipo_racion`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_detalle_menu_intercambio` FOREIGN KEY (`id_intercambio`) REFERENCES `intercambios` (`id_intercambio`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_detalles_menu_intercambio` FOREIGN KEY (`id_intercambio`) REFERENCES `intercambios` (`id_intercambio`) ON DELETE CASCADE;

--
-- Filtros para la tabla `dotacion_menaje`
--
ALTER TABLE `dotacion_menaje`
  ADD CONSTRAINT `dotacion_menaje_ibfk_1` FOREIGN KEY (`id_infraestructura`) REFERENCES `infraestructura` (`id_infraestructura`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `firmas`
--
ALTER TABLE `firmas`
  ADD CONSTRAINT `firmas_ibfk_1` FOREIGN KEY (`id_intercambio`) REFERENCES `intercambios` (`id_intercambio`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_firmas_intercambio` FOREIGN KEY (`id_intercambio`) REFERENCES `intercambios` (`id_intercambio`) ON DELETE CASCADE;

--
-- Filtros para la tabla `firmas_bodega`
--
ALTER TABLE `firmas_bodega`
  ADD CONSTRAINT `firmas_bodega_ibfk_1` FOREIGN KEY (`id_visita`) REFERENCES `visitas_bodega` (`id_visita`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_id_visita` FOREIGN KEY (`id_visita`) REFERENCES `visitas_bodega` (`id_visita`) ON DELETE CASCADE;

--
-- Filtros para la tabla `firmas_infraestructura`
--
ALTER TABLE `firmas_infraestructura`
  ADD CONSTRAINT `firmas_infraestructura_ibfk_1` FOREIGN KEY (`id_infraestructura`) REFERENCES `infraestructura` (`id_infraestructura`) ON DELETE CASCADE;

--
-- Filtros para la tabla `firmas_tecnica`
--
ALTER TABLE `firmas_tecnica`
  ADD CONSTRAINT `firmas_tecnica_ibfk_1` FOREIGN KEY (`id_visita_tecnica`) REFERENCES `visita_tecnica` (`id_visita_tecnica`) ON DELETE CASCADE;

--
-- Filtros para la tabla `firmas_verificacion`
--
ALTER TABLE `firmas_verificacion`
  ADD CONSTRAINT `firmas_verificacion_ibfk_1` FOREIGN KEY (`id_verificacion`) REFERENCES `verificacion_menu` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `fotos_bodega`
--
ALTER TABLE `fotos_bodega`
  ADD CONSTRAINT `fotos_bodega_ibfk_1` FOREIGN KEY (`id_visita`) REFERENCES `visitas_bodega` (`id_visita`) ON DELETE CASCADE;

--
-- Filtros para la tabla `industrializado`
--
ALTER TABLE `industrializado`
  ADD CONSTRAINT `industrializado_ibfk_1` FOREIGN KEY (`id_tipo_racion`) REFERENCES `tiporacion` (`id_tipo_racion`);

--
-- Filtros para la tabla `infraestructura`
--
ALTER TABLE `infraestructura`
  ADD CONSTRAINT `fk_infraestructura_institucion` FOREIGN KEY (`institucion`) REFERENCES `instituciones` (`id_institucion`),
  ADD CONSTRAINT `fk_infraestructura_operador` FOREIGN KEY (`operador`) REFERENCES `operadores` (`id_operador`),
  ADD CONSTRAINT `fk_infraestructura_sede` FOREIGN KEY (`sede`) REFERENCES `sedes` (`id_sede`);

--
-- Filtros para la tabla `instituciones`
--
ALTER TABLE `instituciones`
  ADD CONSTRAINT `fk_id_operador` FOREIGN KEY (`id_operador`) REFERENCES `operadores` (`id_operador`) ON DELETE SET NULL;

--
-- Filtros para la tabla `instituciones_sedes`
--
ALTER TABLE `instituciones_sedes`
  ADD CONSTRAINT `fk_institucion_sedes_intercambio` FOREIGN KEY (`id_intercambio`) REFERENCES `intercambios` (`id_intercambio`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_instituciones_sedes_intercambio` FOREIGN KEY (`id_intercambio`) REFERENCES `intercambios` (`id_intercambio`) ON DELETE CASCADE,
  ADD CONSTRAINT `instituciones_sedes_ibfk_1` FOREIGN KEY (`id_institucion`) REFERENCES `instituciones` (`id_institucion`),
  ADD CONSTRAINT `instituciones_sedes_ibfk_2` FOREIGN KEY (`id_sede`) REFERENCES `sedes` (`id_sede`);

--
-- Filtros para la tabla `intercambios`
--
ALTER TABLE `intercambios`
  ADD CONSTRAINT `intercambios_ibfk_1` FOREIGN KEY (`id_operador`) REFERENCES `operadores` (`id_operador`),
  ADD CONSTRAINT `intercambios_ibfk_2` FOREIGN KEY (`id_tipo_racion`) REFERENCES `tiporacion` (`id_tipo_racion`);

--
-- Filtros para la tabla `jornadaunica`
--
ALTER TABLE `jornadaunica`
  ADD CONSTRAINT `jornadaunica_ibfk_1` FOREIGN KEY (`id_tipo_racion`) REFERENCES `tiporacion` (`id_tipo_racion`);

--
-- Filtros para la tabla `preparadoensitioam`
--
ALTER TABLE `preparadoensitioam`
  ADD CONSTRAINT `fk_tipo_racion` FOREIGN KEY (`id_tipo_racion`) REFERENCES `tiporacion` (`id_tipo_racion`);

--
-- Filtros para la tabla `preparadoensitiopm`
--
ALTER TABLE `preparadoensitiopm`
  ADD CONSTRAINT `preparadoensitiopm_ibfk_1` FOREIGN KEY (`id_tipo_racion`) REFERENCES `tiporacion` (`id_tipo_racion`);

--
-- Filtros para la tabla `puntaje_cumplimiento`
--
ALTER TABLE `puntaje_cumplimiento`
  ADD CONSTRAINT `puntaje_cumplimiento_ibfk_1` FOREIGN KEY (`verificacion_menu_id`) REFERENCES `verificacion_menu` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `respuestas_bodega`
--
ALTER TABLE `respuestas_bodega`
  ADD CONSTRAINT `fk_respuestas_visita` FOREIGN KEY (`id_visita`) REFERENCES `visitas_bodega` (`id_visita`) ON DELETE CASCADE,
  ADD CONSTRAINT `respuestas_bodega_ibfk_1` FOREIGN KEY (`id_visita`) REFERENCES `visitas_bodega` (`id_visita`),
  ADD CONSTRAINT `respuestas_bodega_ibfk_2` FOREIGN KEY (`id_pregunta`) REFERENCES `preguntas_bodega` (`id_pregunta`);

--
-- Filtros para la tabla `respuestas_infraestructura`
--
ALTER TABLE `respuestas_infraestructura`
  ADD CONSTRAINT `fk_respuesta_pregunta` FOREIGN KEY (`id_pregunta`) REFERENCES `preguntas_infraestructura` (`id_pregunta`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `respuestas_infraestructura_ibfk_1` FOREIGN KEY (`id_infraestructura`) REFERENCES `infraestructura` (`id_infraestructura`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `respuestas_infraestructura_ibfk_2` FOREIGN KEY (`id_infraestructura`) REFERENCES `infraestructura` (`id_infraestructura`);

--
-- Filtros para la tabla `respuestas_tecnica`
--
ALTER TABLE `respuestas_tecnica`
  ADD CONSTRAINT `respuestas_tecnica_ibfk_1` FOREIGN KEY (`visita_tecnica_id`) REFERENCES `visita_tecnica` (`id_visita_tecnica`) ON DELETE CASCADE,
  ADD CONSTRAINT `respuestas_tecnica_ibfk_2` FOREIGN KEY (`pregunta_id`) REFERENCES `preguntas_tecnica` (`id_tecnica`);

--
-- Filtros para la tabla `sedes`
--
ALTER TABLE `sedes`
  ADD CONSTRAINT `fk_id_institucion` FOREIGN KEY (`id_institucion`) REFERENCES `instituciones` (`id_institucion`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `temperaturas`
--
ALTER TABLE `temperaturas`
  ADD CONSTRAINT `fk_temperaturas_visita_tecnica` FOREIGN KEY (`id_visita_tecnica`) REFERENCES `visita_tecnica` (`id_visita_tecnica`) ON DELETE CASCADE;

--
-- Filtros para la tabla `toma_peso`
--
ALTER TABLE `toma_peso`
  ADD CONSTRAINT `fk_toma_peso_visita_tecnica` FOREIGN KEY (`id_visita_tecnica`) REFERENCES `visita_tecnica` (`id_visita_tecnica`) ON DELETE CASCADE;

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_operador`) REFERENCES `operadores` (`id_operador`);

--
-- Filtros para la tabla `verificacion_menu`
--
ALTER TABLE `verificacion_menu`
  ADD CONSTRAINT `fk_verificacion_menu_institucion` FOREIGN KEY (`institucion_id`) REFERENCES `instituciones` (`id_institucion`),
  ADD CONSTRAINT `fk_verificacion_menu_operador` FOREIGN KEY (`id_operador`) REFERENCES `operadores` (`id_operador`),
  ADD CONSTRAINT `fk_verificacion_menu_sede` FOREIGN KEY (`sede_id`) REFERENCES `sedes` (`id_sede`),
  ADD CONSTRAINT `fk_verificacion_menu_tipo_racion` FOREIGN KEY (`tipo_racion_id`) REFERENCES `tiporacion` (`id_tipo_racion`);

--
-- Filtros para la tabla `verificacion_menu_detalles`
--
ALTER TABLE `verificacion_menu_detalles`
  ADD CONSTRAINT `verificacion_menu_detalles_ibfk_1` FOREIGN KEY (`verificacion_menu_id`) REFERENCES `verificacion_menu` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `visitas_bodega`
--
ALTER TABLE `visitas_bodega`
  ADD CONSTRAINT `fk_visitas_bodega_operador` FOREIGN KEY (`operador`) REFERENCES `operadores` (`id_operador`);

--
-- Filtros para la tabla `visita_tecnica`
--
ALTER TABLE `visita_tecnica`
  ADD CONSTRAINT `fk_visita_tecnica_institucion` FOREIGN KEY (`institucion_id`) REFERENCES `instituciones` (`id_institucion`),
  ADD CONSTRAINT `fk_visita_tecnica_operador` FOREIGN KEY (`operador`) REFERENCES `operadores` (`id_operador`),
  ADD CONSTRAINT `fk_visita_tecnica_sede` FOREIGN KEY (`sede_id`) REFERENCES `sedes` (`id_sede`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
