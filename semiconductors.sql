-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Июн 08 2023 г., 16:13
-- Версия сервера: 10.4.28-MariaDB
-- Версия PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `semiconductors`
--

-- --------------------------------------------------------

--
-- Структура таблицы `semiconductors`
--

CREATE TABLE `semiconductors` (
  `material` text NOT NULL,
  `dielectric_const` float NOT NULL,
  `mobility_n` float NOT NULL,
  `mobility_p` float NOT NULL,
  `effective_mass_n` float NOT NULL,
  `effective_mass_p` float NOT NULL,
  `dos_effective_mass_n` float NOT NULL,
  `dos_effective_mass_p` float NOT NULL,
  `Eg` text NOT NULL,
  `melting_T` float NOT NULL,
  `Ea` float NOT NULL,
  `Ed` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `semiconductors`
--

INSERT INTO `semiconductors` (`material`, `dielectric_const`, `mobility_n`, `mobility_p`, `effective_mass_n`, `effective_mass_p`, `dos_effective_mass_n`, `dos_effective_mass_p`, `Eg`, `melting_T`, `Ea`, `Ed`) VALUES
('Ge', 16, 3600, 1900, 0.22, 0.34, 0.56, 0.36, '0.742- 4.8*10^(-4)*T^(2)/(T+235)', 1210.6, 0.011, 0.013),
('ZnSe', 8.1, 530, 28, 0.17, 0.6, 0.17, 0.6, '2.81-5.78*10^(-4)*T^(2)/(T+175)', 1790, 0.1236, 0.035),
('CdTe', 10.9, 1050, 80, 0.11, 0.35, 0.11, 0.35, '1.6-4.1∗10^(-4)*T', 1365, 0.0398, 0.0125),
('CdS', 8.96, 350, 15, 0.2, 5.17, 0.2, 5.17, '2.58-5*10^(-4)*T', 1748, 0.8707, 0.0337),
('GaAs', 10.9, 8600, 400, 0.07, 0.45, 0.07, 0.45, '1.52-5.0*10^(-4)*T', 1511, 0.05, 0.01),
('AlAs', 10.9, 1200, 100, 0.18, 0.22, 0.6, 0.22, '2.24-4*10^(-4)*T', 2013, 0.025, 0.0205),
('ZnS', 8.3, 200, 5, 0.25, 0.75, 0.25, 0.75, '3.91-5.41*10^(-4)*T^2/(T+204)', 1830, 0.049, 0.1443),
('Al0.4Ga0.6As', 11.76, 800, 100, 0.1, 0.64, 0.1, 0.64, '1.81-5.41*10^(-4)*T^2/(T+204)', 1579, 0.0629, 0.0095),
('InP', 12.1, 4000, 650, 0.07, 0.4, 0.0962, 0.34, '1.42-4.6*10^(-4)*T^2/(T+204)', 1062, 0.006, 0.037);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `semiconductors`
--
ALTER TABLE `semiconductors`
  ADD UNIQUE KEY `material` (`material`) USING HASH;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
