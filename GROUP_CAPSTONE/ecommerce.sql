-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 21, 2025 at 06:27 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ecommerce`
--

-- --------------------------------------------------------

--
-- Table structure for table `Admins`
--

CREATE TABLE `Admins` (
  `Admin_ID` int(11) NOT NULL,
  `Last_Name` varchar(50) NOT NULL,
  `First_Name` varchar(50) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Pass` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Cart`
--

CREATE TABLE `Cart` (
  `cart_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Cart`
--

INSERT INTO `Cart` (`cart_id`, `user_id`, `product_id`, `quantity`) VALUES
(57, 1, 1, 19),
(58, 1, 2, 13),
(59, 1, 3, 12),
(60, 1, 4, 20),
(63, 4, 1, 1),
(64, 4, 2, 1),
(65, 4, 3, 1),
(66, 4, 4, 2),
(67, 4, 5, 2),
(68, 4, 6, 2),
(72, 4, 7, 1),
(73, 4, 8, 1);

-- --------------------------------------------------------

--
-- Table structure for table `Contacts`
--

CREATE TABLE `Contacts` (
  `Contact_id` int(11) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Subject` varchar(255) NOT NULL,
  `Contact_desc` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Order_info`
--

CREATE TABLE `Order_info` (
  `Order_ID` int(11) NOT NULL,
  `Cust_ID` int(11) DEFAULT NULL,
  `Username` varchar(50) DEFAULT NULL,
  `Product_ID` int(11) DEFAULT NULL,
  `Del_address` varchar(255) NOT NULL,
  `Del_date` date NOT NULL,
  `Payment_method` enum('Credit Card','PayPal','Cash on Delivery') NOT NULL,
  `Actions` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Products`
--

CREATE TABLE `Products` (
  `Product_ID` int(11) NOT NULL,
  `Product_Name` varchar(100) NOT NULL,
  `Product_Desc` text NOT NULL,
  `picture` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Products`
--

INSERT INTO `Products` (`Product_ID`, `Product_Name`, `Product_Desc`, `picture`, `price`) VALUES
(1, 'Beautiful White Dress', 'Beautiful White dress, perfect for any occasions.', 'static/img/product-1.jpg', 123.00),
(2, 'Jackets for teens', 'Jacket for teens, perfect for passion', 'static/img/product-2.jpg', 123.00),
(3, 'Scarf for men', 'Scarf for men, perfect for flexing. If you\'re handsome you\'ll buy one.', 'static/img/product-3.jpg', 200.00),
(4, 'Black sleeves mini dress', 'Perfect if you want to flex your beauty.', 'static/img/product-4.jpg', 150.00),
(5, 'Multi-colored t-shirt', 'Can be used for events', 'static/img/product-5.jpg', 50.00),
(6, 'Groom suit', 'Perfect for wedding events, flexing and for handsome men.', 'static/img/product-6.jpg', 1000.00),
(7, 'Girl Fasion Suit', 'Perfect for showcasing your beauty for everyone.', 'static/img/product-7.jpg', 250.00),
(8, 'Soffny Boy Plain', 'Great for kids.', 'static/img/product-8.jpg', 150.00),
(9, 'Jacket for women', 'Perfect for flexing your beauty.', 'static/img/product-9.jpg', 400.00);

-- --------------------------------------------------------

--
-- Table structure for table `Users`
--

CREATE TABLE `Users` (
  `Cust_ID` int(11) NOT NULL,
  `Last_Name` varchar(50) NOT NULL,
  `First_Name` varchar(50) NOT NULL,
  `Gender` enum('Male','Female','Other') NOT NULL,
  `Phone_number` varchar(20) DEFAULT NULL,
  `UserName` varchar(50) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Users`
--

INSERT INTO `Users` (`Cust_ID`, `Last_Name`, `First_Name`, `Gender`, `Phone_number`, `UserName`, `Email`, `Password`) VALUES
(1, 'jayme', 'selwyn', 'Male', '3242', 'gwapo', 'gwapo@gmail.com', 'gwapo'),
(4, 'pinakagwapo', 'Gwapo ako', 'Male', '09693052186', 'gwapoako', 'gwapoako@gmail.com', 'gwapoako');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Admins`
--
ALTER TABLE `Admins`
  ADD PRIMARY KEY (`Admin_ID`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- Indexes for table `Cart`
--
ALTER TABLE `Cart`
  ADD PRIMARY KEY (`cart_id`),
  ADD UNIQUE KEY `unique_user_product` (`user_id`,`product_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `Contacts`
--
ALTER TABLE `Contacts`
  ADD PRIMARY KEY (`Contact_id`);

--
-- Indexes for table `Order_info`
--
ALTER TABLE `Order_info`
  ADD PRIMARY KEY (`Order_ID`),
  ADD KEY `Cust_ID` (`Cust_ID`),
  ADD KEY `Product_ID` (`Product_ID`);

--
-- Indexes for table `Products`
--
ALTER TABLE `Products`
  ADD PRIMARY KEY (`Product_ID`);

--
-- Indexes for table `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`Cust_ID`),
  ADD UNIQUE KEY `UserName` (`UserName`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Admins`
--
ALTER TABLE `Admins`
  MODIFY `Admin_ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Cart`
--
ALTER TABLE `Cart`
  MODIFY `cart_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=74;

--
-- AUTO_INCREMENT for table `Contacts`
--
ALTER TABLE `Contacts`
  MODIFY `Contact_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Order_info`
--
ALTER TABLE `Order_info`
  MODIFY `Order_ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Products`
--
ALTER TABLE `Products`
  MODIFY `Product_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `Users`
--
ALTER TABLE `Users`
  MODIFY `Cust_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Cart`
--
ALTER TABLE `Cart`
  ADD CONSTRAINT `Cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`Cust_ID`) ON DELETE CASCADE,
  ADD CONSTRAINT `Cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `Products` (`Product_ID`) ON DELETE CASCADE;

--
-- Constraints for table `Order_info`
--
ALTER TABLE `Order_info`
  ADD CONSTRAINT `Order_info_ibfk_1` FOREIGN KEY (`Cust_ID`) REFERENCES `Users` (`Cust_ID`) ON DELETE CASCADE,
  ADD CONSTRAINT `Order_info_ibfk_2` FOREIGN KEY (`Product_ID`) REFERENCES `Products` (`Product_ID`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
