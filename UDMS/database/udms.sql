-- phpMyAdmin SQL Dump
-- version 4.8.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 18, 2019 at 08:14 PM
-- Server version: 10.1.32-MariaDB
-- PHP Version: 7.2.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `udms`
--

-- --------------------------------------------------------

--
-- Table structure for table `amatch`
--

CREATE TABLE `amatch` (
  `match_id` int(11) NOT NULL,
  `match_name` varchar(30) NOT NULL,
  `date` date DEFAULT NULL,
  `win` int(11) DEFAULT NULL,
  `side` int(11) NOT NULL,
  `opponent` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `amatch`
--

INSERT INTO `amatch` (`match_id`, `match_name`, `date`, `win`, `side`, `opponent`) VALUES
(1, 'train', '2019-05-12', 1, 1, 'UCCG'),
(2, 'better train', '2019-05-13', 0, 0, 'HKBU');

-- --------------------------------------------------------

--
-- Table structure for table `assignment`
--

CREATE TABLE `assignment` (
  `a_id` int(11) NOT NULL,
  `a_date` date DEFAULT NULL,
  `title` varchar(30) DEFAULT NULL,
  `detail` text,
  `create_id` int(11) NOT NULL,
  `dueDate` date NOT NULL,
  `dueTime` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `assignment`
--

INSERT INTO `assignment` (`a_id`, `a_date`, `title`, `detail`, `create_id`, `dueDate`, `dueTime`) VALUES
(1, '2019-05-06', 'first draft', 'just write something and nobody will see it', 1730026109, '2019-05-22', '09:00:00'),
(2, '2019-05-13', 'beautiful', 'interesting we are all gonna die nobody will escape', 1730026119, '2019-05-22', '11:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `attend`
--

CREATE TABLE `attend` (
  `id` int(11) DEFAULT NULL,
  `a_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `attend`
--

INSERT INTO `attend` (`id`, `a_id`) VALUES
(1730026119, 1),
(1730026028, 2),
(1730026119, 173002611920195180),
(1730026119, 173002611920195181),
(1730026119, 173002611920195182);

-- --------------------------------------------------------

--
-- Table structure for table `attendance_record`
--

CREATE TABLE `attendance_record` (
  `a_id` bigint(20) NOT NULL,
  `status` int(11) DEFAULT NULL,
  `time_slot` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `attendance_record`
--

INSERT INTO `attendance_record` (`a_id`, `status`, `time_slot`) VALUES
(1, 1, '2019-05-15 00:00:00'),
(2, 0, '2019-05-15 00:00:00'),
(173002611920195180, 0, '2019-05-19 02:12:47'),
(173002611920195181, 3, '2019-05-19 02:13:06'),
(173002611920195182, 2, '2019-05-19 02:13:17');

-- --------------------------------------------------------

--
-- Table structure for table `belong_to`
--

CREATE TABLE `belong_to` (
  `id` int(11) NOT NULL,
  `group_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `belong_to`
--

INSERT INTO `belong_to` (`id`, `group_id`) VALUES
(1730026109, 0),
(1730026119, 1),
(1730026120, 1);

-- --------------------------------------------------------

--
-- Table structure for table `comes_from`
--

CREATE TABLE `comes_from` (
  `a_id` int(11) NOT NULL,
  `m_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `comes_from`
--

INSERT INTO `comes_from` (`a_id`, `m_id`) VALUES
(1, 1),
(2, 2);

-- --------------------------------------------------------

--
-- Table structure for table `dates`
--

CREATE TABLE `dates` (
  `date_id` int(11) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dates`
--

INSERT INTO `dates` (`date_id`, `date`) VALUES
(1, '2019-05-05'),
(2, '2019-05-06');

-- --------------------------------------------------------

--
-- Table structure for table `dates_events`
--

CREATE TABLE `dates_events` (
  `dates_events_id` int(11) NOT NULL,
  `date_id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dates_events`
--

INSERT INTO `dates_events` (`dates_events_id`, `date_id`, `event_id`) VALUES
(1, 1, 1),
(2, 2, 2);

-- --------------------------------------------------------

--
-- Table structure for table `document`
--

CREATE TABLE `document` (
  `d_id` int(11) NOT NULL,
  `doc` blob,
  `doc_name` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `FIRST_NAME` char(20) NOT NULL,
  `LAST_NAME` char(20) DEFAULT NULL,
  `AGE` int(11) DEFAULT NULL,
  `SEX` char(1) DEFAULT NULL,
  `INCOME` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`FIRST_NAME`, `LAST_NAME`, `AGE`, `SEX`, `INCOME`) VALUES
('Mary', 'Smith', 19, 'F', 2000),
('Gary', 'Lee', 21, 'M', 2000),
('Becky', 'Bucked', 21, 'F', 2800);

-- --------------------------------------------------------

--
-- Table structure for table `events`
--

CREATE TABLE `events` (
  `event_id` int(11) NOT NULL,
  `event_name` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `events`
--

INSERT INTO `events` (`event_id`, `event_name`) VALUES
(1, 'Mid-term exam'),
(2, 'Staff annual party');

-- --------------------------------------------------------

--
-- Table structure for table `file_contents`
--

CREATE TABLE `file_contents` (
  `file_id` int(11) NOT NULL,
  `name` varchar(300) DEFAULT NULL,
  `data` blob
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `has`
--

CREATE TABLE `has` (
  `id` int(11) NOT NULL,
  `r_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `has`
--

INSERT INTO `has` (`id`, `r_id`) VALUES
(1730026109, 1),
(1730026109, 2);

-- --------------------------------------------------------

--
-- Table structure for table `meeting`
--

CREATE TABLE `meeting` (
  `m_id` int(11) NOT NULL,
  `theme` varchar(20) DEFAULT NULL,
  `meeting_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `meeting_note`
--

CREATE TABLE `meeting_note` (
  `n_id` int(11) NOT NULL,
  `m_id` int(11) NOT NULL,
  `note` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `own`
--

CREATE TABLE `own` (
  `id` int(11) NOT NULL,
  `info_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `own`
--

INSERT INTO `own` (`id`, `info_id`) VALUES
(1730026109, 0),
(1730026119, 1),
(1730026044, 2),
(1730026028, 3),
(1730026120, 4),
(1730026121, 5),
(1730026122, 6),
(1730026123, 7),
(1730026124, 8),
(1730026125, 9),
(1730026126, 10),
(1730026127, 11),
(1730026128, 12),
(1730026129, 13),
(1730026130, 14),
(1730026131, 15),
(1730026132, 16);

-- --------------------------------------------------------

--
-- Table structure for table `personal_information`
--

CREATE TABLE `personal_information` (
  `info_id` int(11) NOT NULL,
  `grade` varchar(5) DEFAULT NULL,
  `major` varchar(20) DEFAULT NULL,
  `last_name` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `personal_information`
--

INSERT INTO `personal_information` (`info_id`, `grade`, `major`, `last_name`) VALUES
(0, '1.5', 'CST', 'Ng'),
(1, '1', 'CST', 'Ho'),
(2, '2', 'CST', 'Wong'),
(3, '0.5', 'CST', 'Li'),
(4, '2.5', 'CST', 'Wu'),
(5, '1', 'CST', 'Sam'),
(6, '2', 'CTV', 'Ng'),
(7, '2', 'CST', 'Luo'),
(8, '1.2', 'APSY', 'Lu'),
(9, '0.2', 'CST', 'Lam'),
(10, '3', 'CST', 'Su'),
(11, '4', 'CST', 'Lau'),
(12, '2', 'CST', 'Chan'),
(13, '1', 'CST', 'Yu'),
(14, '2.3', 'CST', 'Luo'),
(15, '3.2', 'CST', 'Kuang'),
(16, '1.6', 'CST', 'Dang');

-- --------------------------------------------------------

--
-- Table structure for table `record`
--

CREATE TABLE `record` (
  `r_id` int(11) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_mvp` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `record`
--

INSERT INTO `record` (`r_id`, `position`, `is_mvp`) VALUES
(1, 1, 0),
(2, 2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `submission`
--

CREATE TABLE `submission` (
  `a_id` int(11) NOT NULL,
  `d_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `submit`
--

CREATE TABLE `submit` (
  `id` int(11) NOT NULL,
  `as_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `take_part`
--

CREATE TABLE `take_part` (
  `match_id` int(11) NOT NULL,
  `r_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `password` varchar(16) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `password`, `name`) VALUES
(1730026028, '123456', 'Wildman'),
(1730026044, '123456', 'Rory'),
(1730026109, '123456', 'Qizheng'),
(1730026119, '123456', 'Shuyang'),
(1730026120, '123123123', 'HaaaHa'),
(1730026121, '123456', 'Test2'),
(1730026122, '123456', 'Shuyang'),
(1730026123, '123456', 'Test3'),
(1730026124, '123456', 'Test4'),
(1730026125, '123456', 'Test5'),
(1730026126, '123456', 'Test6'),
(1730026127, '123456', 'Test8'),
(1730026128, '123456', 'Test7'),
(1730026129, '123456', 'Test9'),
(1730026130, '123456', 'Test10'),
(1730026131, '123456', 'Test11'),
(1730026132, '123456', 'Test12');

-- --------------------------------------------------------

--
-- Table structure for table `user_group`
--

CREATE TABLE `user_group` (
  `group_id` int(11) NOT NULL,
  `group_name` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_group`
--

INSERT INTO `user_group` (`group_id`, `group_name`) VALUES
(0, 'user'),
(1, 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `amatch`
--
ALTER TABLE `amatch`
  ADD PRIMARY KEY (`match_id`);

--
-- Indexes for table `assignment`
--
ALTER TABLE `assignment`
  ADD PRIMARY KEY (`a_id`),
  ADD KEY `id` (`create_id`);

--
-- Indexes for table `attend`
--
ALTER TABLE `attend`
  ADD PRIMARY KEY (`a_id`);

--
-- Indexes for table `attendance_record`
--
ALTER TABLE `attendance_record`
  ADD PRIMARY KEY (`a_id`);

--
-- Indexes for table `belong_to`
--
ALTER TABLE `belong_to`
  ADD PRIMARY KEY (`id`),
  ADD KEY `group_id` (`group_id`),
  ADD KEY `id` (`id`);

--
-- Indexes for table `comes_from`
--
ALTER TABLE `comes_from`
  ADD PRIMARY KEY (`a_id`),
  ADD KEY `m_id` (`m_id`),
  ADD KEY `a_id` (`a_id`);

--
-- Indexes for table `document`
--
ALTER TABLE `document`
  ADD PRIMARY KEY (`d_id`);

--
-- Indexes for table `file_contents`
--
ALTER TABLE `file_contents`
  ADD PRIMARY KEY (`file_id`);

--
-- Indexes for table `has`
--
ALTER TABLE `has`
  ADD PRIMARY KEY (`id`,`r_id`),
  ADD KEY `match_id` (`r_id`),
  ADD KEY `id` (`id`);

--
-- Indexes for table `meeting`
--
ALTER TABLE `meeting`
  ADD PRIMARY KEY (`m_id`);

--
-- Indexes for table `meeting_note`
--
ALTER TABLE `meeting_note`
  ADD PRIMARY KEY (`n_id`,`m_id`);

--
-- Indexes for table `own`
--
ALTER TABLE `own`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inf_id` (`info_id`);

--
-- Indexes for table `personal_information`
--
ALTER TABLE `personal_information`
  ADD PRIMARY KEY (`info_id`);

--
-- Indexes for table `record`
--
ALTER TABLE `record`
  ADD PRIMARY KEY (`r_id`);

--
-- Indexes for table `submission`
--
ALTER TABLE `submission`
  ADD PRIMARY KEY (`a_id`,`d_id`);

--
-- Indexes for table `submit`
--
ALTER TABLE `submit`
  ADD PRIMARY KEY (`id`,`as_id`),
  ADD KEY `as_id` (`as_id`);

--
-- Indexes for table `take_part`
--
ALTER TABLE `take_part`
  ADD PRIMARY KEY (`match_id`,`r_id`),
  ADD KEY `r_id` (`r_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_group`
--
ALTER TABLE `user_group`
  ADD PRIMARY KEY (`group_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attend`
--
ALTER TABLE `attend`
  MODIFY `a_id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2147483647;

--
-- AUTO_INCREMENT for table `attendance_record`
--
ALTER TABLE `attendance_record`
  MODIFY `a_id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2147483647;

--
-- AUTO_INCREMENT for table `file_contents`
--
ALTER TABLE `file_contents`
  MODIFY `file_id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
