-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 24, 2020 at 09:57 AM
-- Server version: 10.4.6-MariaDB
-- PHP Version: 7.3.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ka_stei`
--

-- --------------------------------------------------------

--
-- Table structure for table `dokumen`
--

CREATE TABLE `dokumen` (
  `ID_Permintaan` int(11) NOT NULL,
  `dokumen_tanpa_ttd` blob NOT NULL,
  `dokumen_ttd` blob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dokumen`
--

INSERT INTO `dokumen` (`ID_Permintaan`, `dokumen_tanpa_ttd`, `dokumen_ttd`) VALUES
(4, '', NULL),
(5, 0x31303130313031303130313031303130313030303030303030313131313131313131, 0x31303130313031303130313031303130313030303030303030313131313131313131);

-- --------------------------------------------------------

--
-- Table structure for table `mahasiswa`
--

CREATE TABLE `mahasiswa` (
  `Nama` varchar(30) NOT NULL,
  `NIM` int(8) NOT NULL,
  `Jurusan` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `mahasiswa`
--

INSERT INTO `mahasiswa` (`Nama`, `NIM`, `Jurusan`) VALUES
('Madiha Ainayya', 18218010, 'STI'),
('Christovito Hidajat', 18218043, 'STI');

-- --------------------------------------------------------

--
-- Table structure for table `permintaan`
--

CREATE TABLE `permintaan` (
  `ID_Permintaan` int(4) NOT NULL,
  `Nama` varchar(30) NOT NULL,
  `NIM` int(8) NOT NULL,
  `Jurusan` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `permintaan`
--

INSERT INTO `permintaan` (`ID_Permintaan`, `Nama`, `NIM`, `Jurusan`) VALUES
(4, 'Madiha Ainayya', 18218010, 'STI'),
(5, 'Christovito Hidajat', 18218043, 'STI');

-- --------------------------------------------------------

--
-- Table structure for table `permintaan_surat_rekomendasi`
--

CREATE TABLE `permintaan_surat_rekomendasi` (
  `ID_Permintaan` int(4) NOT NULL,
  `Instansi_Tujuan` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `permintaan_surat_rekomendasi`
--

INSERT INTO `permintaan_surat_rekomendasi` (`ID_Permintaan`, `Instansi_Tujuan`) VALUES
(4, 'Pertamina'),
(5, 'Djarum');

-- --------------------------------------------------------

--
-- Table structure for table `permintaan_transkrip`
--

CREATE TABLE `permintaan_transkrip` (
  `ID_Permintaan` int(4) NOT NULL,
  `Semester` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `status_permintaan`
--

CREATE TABLE `status_permintaan` (
  `ID_Permintaan` int(4) NOT NULL,
  `Status` varchar(25) NOT NULL DEFAULT 'sedang divalidasi'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `status_permintaan`
--

INSERT INTO `status_permintaan` (`ID_Permintaan`, `Status`) VALUES
(4, 'sedang divalidasi'),
(5, 'Selesai');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `dokumen`
--
ALTER TABLE `dokumen`
  ADD PRIMARY KEY (`ID_Permintaan`);

--
-- Indexes for table `mahasiswa`
--
ALTER TABLE `mahasiswa`
  ADD PRIMARY KEY (`NIM`);

--
-- Indexes for table `permintaan`
--
ALTER TABLE `permintaan`
  ADD PRIMARY KEY (`ID_Permintaan`),
  ADD KEY `NIM` (`NIM`);

--
-- Indexes for table `permintaan_surat_rekomendasi`
--
ALTER TABLE `permintaan_surat_rekomendasi`
  ADD PRIMARY KEY (`ID_Permintaan`);

--
-- Indexes for table `permintaan_transkrip`
--
ALTER TABLE `permintaan_transkrip`
  ADD PRIMARY KEY (`ID_Permintaan`);

--
-- Indexes for table `status_permintaan`
--
ALTER TABLE `status_permintaan`
  ADD PRIMARY KEY (`ID_Permintaan`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `dokumen`
--
ALTER TABLE `dokumen`
  MODIFY `ID_Permintaan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `permintaan`
--
ALTER TABLE `permintaan`
  MODIFY `ID_Permintaan` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `permintaan_surat_rekomendasi`
--
ALTER TABLE `permintaan_surat_rekomendasi`
  MODIFY `ID_Permintaan` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `permintaan_transkrip`
--
ALTER TABLE `permintaan_transkrip`
  MODIFY `ID_Permintaan` int(4) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `status_permintaan`
--
ALTER TABLE `status_permintaan`
  MODIFY `ID_Permintaan` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
