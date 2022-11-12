-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 12, 2022 at 09:31 PM
-- Server version: 10.4.19-MariaDB
-- PHP Version: 7.4.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `emergency_services_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `psw` varchar(255) NOT NULL,
  `account_type` varchar(255) NOT NULL,
  `full_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `email`, `psw`, `account_type`, `full_name`) VALUES
(1, 'maleesha@gmail.com', '25d55ad283aa400af464c76d713c07ad', 'admin', 'Maleesha');

-- --------------------------------------------------------

--
-- Table structure for table `branches`
--

CREATE TABLE `branches` (
  `id` int(255) NOT NULL,
  `branch_id` varchar(255) NOT NULL,
  `department_id` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `emergency_number` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `map_url` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `branches`
--

INSERT INTO `branches` (`id`, `branch_id`, `department_id`, `location`, `emergency_number`, `address`, `map_url`) VALUES
(4, '20220821498124', 'Hospital2022082211406184', 'Homagama', '0112452632', 'Homagama', 'https://goo.gl/maps/UzuDn2t5sBqCANCC7'),
(5, '2022082252092101', 'Hospital2022082211406184', 'Galle', '0914526532', 'Galle Town', 'https://goo.gl/maps/i26vAai2GXniSMHp9');

-- --------------------------------------------------------

--
-- Table structure for table `branch_users`
--

CREATE TABLE `branch_users` (
  `id` int(255) NOT NULL,
  `branch_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `psw` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `branch_users`
--

INSERT INTO `branch_users` (`id`, `branch_id`, `name`, `email`, `psw`) VALUES
(2, '20220821498124', 'Maleesha S', 'maleeshaspolice@gmail.com', '25d55ad283aa400af464c76d713c07ad'),
(4, '20220821498124', 'Maleesha Hospital', 'maleeshahospital@gmail.com', '25d55ad283aa400af464c76d713c07ad'),
(5, '2022082252092100', 'Sithu Hospital', 'sithuhospital@gmail.com', '25d55ad283aa400af464c76d713c07ad');

-- --------------------------------------------------------

--
-- Table structure for table `departments`
--

CREATE TABLE `departments` (
  `id` int(255) NOT NULL,
  `department_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `emergency_number` varchar(255) NOT NULL,
  `web_link` varchar(255) NOT NULL,
  `address` varchar(500) NOT NULL,
  `description` varchar(2000) NOT NULL,
  `thumbnail` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `departments`
--

INSERT INTO `departments` (`id`, `department_id`, `name`, `emergency_number`, `web_link`, `address`, `description`, `thumbnail`) VALUES
(1, '2147483647', 'Police', '119', 'www.police.lk', 'Colombo', 'Sri Lanka Police Department', '20220330933613.png'),
(5, 'Hospital2022082211406184', 'Hospital', '0112452632', 'www.hospital.gov.lk', 'Colombo', 'Sri Lanka General Hospital', 'Hospital2022082211406184.png');

-- --------------------------------------------------------

--
-- Table structure for table `inquiries`
--

CREATE TABLE `inquiries` (
  `auto_id` int(255) NOT NULL,
  `id` varchar(255) NOT NULL,
  `details` varchar(500) NOT NULL,
  `location` varchar(255) NOT NULL,
  `contact` varchar(255) NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `branch` varchar(255) NOT NULL,
  `lat` varchar(255) NOT NULL,
  `lon` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `date` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `inquiry_comments`
--

CREATE TABLE `inquiry_comments` (
  `id` int(255) NOT NULL,
  `inquiry_id` varchar(255) NOT NULL,
  `comment` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `inquiry_images`
--

CREATE TABLE `inquiry_images` (
  `id` int(255) NOT NULL,
  `inquiry_id` varchar(255) NOT NULL,
  `image_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `inquiry_video`
--

CREATE TABLE `inquiry_video` (
  `id` int(11) NOT NULL,
  `inquiry_id` varchar(255) NOT NULL,
  `video_link` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `inqury_actions`
--

CREATE TABLE `inqury_actions` (
  `id` int(255) NOT NULL,
  `inquiry_id` varchar(255) NOT NULL,
  `branch_id` varchar(255) NOT NULL,
  `branch_user_id` varchar(255) NOT NULL,
  `action` varchar(500) NOT NULL,
  `date_time` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `predictions`
--

CREATE TABLE `predictions` (
  `id` int(255) NOT NULL,
  `inquiry_id` varchar(255) NOT NULL,
  `image_id` varchar(255) NOT NULL,
  `prediction` varchar(255) NOT NULL,
  `accuracy` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `nic` varchar(255) NOT NULL,
  `number` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `psw` varchar(255) NOT NULL,
  `profile_pic` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `first_name`, `last_name`, `email`, `nic`, `number`, `address`, `psw`, `profile_pic`) VALUES
(1, 'Maleesha', 'Sulakshana', 'maleesha@gmail.com', '982760747V', '0764852852', '406/5/1, Pitipana North Homagama', '25d55ad283aa400af464c76d713c07ad', '1.png'),
(3, 'Sulakshana', 'Jayasinghe', 'sulakshana@gmail.com', '982760747V', '0767950600', '406/5/1, Pitipana North Homagama', '25d55ad283aa400af464c76d713c07ad', ''),
(5, 'Jayasinghe', 'Sulakshana', 'jayasinghesulakshana@gmail.com', '982760747V', '0765241365', '406/5/1, Colombo', '25d55ad283aa400af464c76d713c07ad', ''),
(6, 'Sithumini', 'Navodya', 'nsithumini96@gmail.com', '965236548V', '0715828021', 'Galle', '25d55ad283aa400af464c76d713c07ad', '6.png');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `branches`
--
ALTER TABLE `branches`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `branch_users`
--
ALTER TABLE `branch_users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `departments`
--
ALTER TABLE `departments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `inquiries`
--
ALTER TABLE `inquiries`
  ADD PRIMARY KEY (`auto_id`);

--
-- Indexes for table `inquiry_comments`
--
ALTER TABLE `inquiry_comments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `inquiry_images`
--
ALTER TABLE `inquiry_images`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `inquiry_video`
--
ALTER TABLE `inquiry_video`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `inqury_actions`
--
ALTER TABLE `inqury_actions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `predictions`
--
ALTER TABLE `predictions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `branches`
--
ALTER TABLE `branches`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `branch_users`
--
ALTER TABLE `branch_users`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `departments`
--
ALTER TABLE `departments`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `inquiries`
--
ALTER TABLE `inquiries`
  MODIFY `auto_id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `inquiry_comments`
--
ALTER TABLE `inquiry_comments`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `inquiry_images`
--
ALTER TABLE `inquiry_images`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=59;

--
-- AUTO_INCREMENT for table `inquiry_video`
--
ALTER TABLE `inquiry_video`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `inqury_actions`
--
ALTER TABLE `inqury_actions`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `predictions`
--
ALTER TABLE `predictions`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
