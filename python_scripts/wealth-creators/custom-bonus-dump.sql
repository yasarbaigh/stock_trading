-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.0.38-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             9.5.0.5196
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping structure for table nse_stats.stock_corporate_actions
CREATE TABLE IF NOT EXISTS `stock_corporate_actions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nse_code` varchar(50) NOT NULL,
  `action` enum('BONUS','SPLIT','START','EXIT') NOT NULL,
  `event_date` date NOT NULL,
  `ratio_prefix` int(11) NOT NULL,
  `ratio_suffix` int(11) NOT NULL,
  `pre_event_price` float NOT NULL,
  `post_event_price` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;

-- Dumping data for table nse_stats.stock_corporate_actions: ~4 rows (approximately)
/*!40000 ALTER TABLE `stock_corporate_actions` DISABLE KEYS */;
INSERT INTO `stock_corporate_actions` (`id`, `nse_code`, `action`, `event_date`, `ratio_prefix`, `ratio_suffix`, `pre_event_price`, `post_event_price`) VALUES
	(1, 'HCLTECH', 'BONUS', '2015-03-01', 1, 1, 25, 25),
	(2, 'HCLTECH', 'BONUS', '2019-12-01', 1, 1, 25, 65),
	(3, 'INFY', 'BONUS', '2014-12-01', 1, 1, 1120, 1120),
	(4, 'INFY', 'BONUS', '2015-06-01', 1, 1, 1120, 1120),
	(5, 'INFY', 'BONUS', '2018-09-01', 1, 1, 1120, 1120),
	(9, 'AVANTIFEED', 'SPLIT', '2015-11-01', 10, 2, 1120, 1120),
	(10, 'AVANTIFEED', 'BONUS', '2018-06-01', 1, 2, 1120, 1120),
	(11, 'AVANTIFEED', 'SPLIT', '2018-06-01', 2, 1, 1120, 1120),
	(12, 'TTKPRESTIG', 'BONUS', '2019-05-01', 1, 5, 1120, 1120),
	(13, 'MOTHERSUMI ', 'BONUS', '2012-10-01', 1, 2, 1120, 1120),
	(14, 'MOTHERSUMI ', 'BONUS', '2013-12-01', 1, 2, 1120, 1120),
	(15, 'MOTHERSUMI ', 'BONUS', '2015-07-01', 1, 2, 1120, 1120),
	(16, 'MOTHERSUMI ', 'BONUS', '2017-07-01', 1, 2, 1120, 1120),
	(17, 'MOTHERSUMI ', 'BONUS', '2018-10-01', 1, 2, 1120, 1120),
	(18, 'ASTRAL ', 'SPLIT', '2010-09-01', 10, 5, 1120, 1120),
	(19, 'ASTRAL ', 'SPLIT', '2013-09-01', 5, 2, 1120, 1120),
	(20, 'ASTRAL ', 'SPLIT', '2014-09-01', 2, 1, 1120, 1120),
	(21, 'ASTRAL ', 'BONUS', '2019-09-01', 1, 4, 1120, 1120);
/*!40000 ALTER TABLE `stock_corporate_actions` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
