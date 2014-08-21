-- MySQL dump 10.13  Distrib 5.1.70, for debian-linux-gnu (i486)
--
-- Host: 10.7.16.11    Database: pamc
-- ------------------------------------------------------
-- Server version	5.1.67-0ubuntu0.10.04.1-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `pagespeed_netservicecode`
--

DROP TABLE IF EXISTS `pagespeed_netservicecode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pagespeed_netservicecode` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `netservice_name` varchar(255) NOT NULL,
  `netservice_id` varchar(75) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `netservice_id` (`netservice_id`),
  KEY `pagespeed_netservicecode_1d228a48` (`netservice_name`)
) ENGINE=MyISAM AUTO_INCREMENT=71 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagespeed_netservicecode`
--

LOCK TABLES `pagespeed_netservicecode` WRITE;
/*!40000 ALTER TABLE `pagespeed_netservicecode` DISABLE KEYS */;
INSERT INTO `pagespeed_netservicecode` VALUES (1,'CERNET数据中心','83'),(2,'帝联科技','78'),(3,'合聚数字技术','80'),(4,'网联无限','81'),(5,'大河数据中心苏州桥机房','93'),(6,'Brazil Lacnic','95'),(7,'其它','0'),(8,'中国电信','1'),(9,'中国网通','2'),(10,'中国铁通','4'),(11,'有线通','8'),(12,'中国联通','16'),(13,'中国教育网','17'),(14,'中国移动','18'),(15,'海泰宽带','94'),(16,'北京市歌华宽带','20'),(17,'长城宽带','21'),(18,'深圳天威视讯','22'),(19,'中国广电宽带','23'),(20,'北京电信通','24'),(21,'台湾省HINET','28'),(22,'方正宽带','26'),(23,'星和宽带','27'),(24,'韩国Hanaro电信','30'),(25,'珠江宽频','31'),(26,'香港Cable TV ','32'),(27,'香港HGC','33'),(28,'香港PCCW Limited','34'),(29,'JAPAN Telecom','37'),(30,'Korea Telecom','38'),(31,'US Cox','39'),(32,'北京光环新网','40'),(33,'JAPAN NTT','41'),(34,'Canada Rogers','44'),(35,'Spain COLT','43'),(36,'Germany Teleforica','45'),(37,'Singapore SingNet','46'),(38,'Australia Telstra','47'),(39,'UK Virgin Media','48'),(40,'Malaysia Telekom','49'),(41,'澳门电讯','50'),(42,'百灵宽带','51'),(43,'Vietnam Telecom','52'),(44,'油田宽带','53'),(45,'香港City Telecom ','54'),(46,'US Tulsa','55'),(47,'US Comcast Cable','56'),(48,'Philippines Globe Telecom','57'),(49,'Polish Telecom','58'),(50,'视讯宽带','59'),(51,'中电华通','60'),(52,'中电飞华','61'),(53,'世纪互联','62'),(54,'赛尔网络','63'),(55,'网宿科技','64'),(56,'金桥网','65'),(57,'科技网','66'),(58,'JAPAN KDDI','67'),(59,'润科通信','69'),(60,'世纪华晨','70'),(61,'互联通','71'),(62,'France Free SAS','72'),(63,'Korea SK','73'),(64,'US Road Runner','74'),(65,'南凌科技','75'),(66,'New Zealand Telecom','76'),(67,'电子政务网','77'),(68,'Singapore SingTel','92'),(69,'北京首信网','82'),(70,'US Telia','90');
/*!40000 ALTER TABLE `pagespeed_netservicecode` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-08-21 18:25:14
