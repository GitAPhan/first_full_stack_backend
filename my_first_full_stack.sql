-- MariaDB dump 10.19  Distrib 10.6.5-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: my_first_full_stack
-- ------------------------------------------------------
-- Server version	10.6.5-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `candy`
--

DROP TABLE IF EXISTS `candy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `candy` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(255) NOT NULL,
  `user_id` int(10) unsigned NOT NULL DEFAULT 2,
  PRIMARY KEY (`id`),
  KEY `candy_FK` (`user_id`),
  CONSTRAINT `candy_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `candy`
--

LOCK TABLES `candy` WRITE;
/*!40000 ALTER TABLE `candy` DISABLE KEYS */;
INSERT INTO `candy` VALUES (1,'candy1','description of candy',1),(2,'candy2','description of candy',1),(4,'candy4','description of candy',2),(5,'candy_2','new patch request from postman',2),(6,'candy_postman1','description submitted by postman',2),(7,'candy_postman2','new patch request from postman',2),(9,'candy_postman7','description submitted by postman',2);
/*!40000 ALTER TABLE `candy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `login_token` varchar(100) NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `login_un` (`login_token`),
  KEY `login_FK` (`user_id`),
  CONSTRAINT `login_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES (2,'K4adweUmPdPSwSD-H8Iisb8CbfiNnGG-eXZwhBsUaPQ',2,'2022-02-09 18:22:44'),(3,'oC4hIqWkPI713lb4L-cVq9zVvRw7YhpS2powqVRkYCM',2,'2022-02-09 18:25:16'),(4,'ufsgZfhaofseu5ES1atzq-2BJ8rDalDPC6mZOv3DiC0',2,'2022-02-09 18:28:28'),(5,'y8OjYV84iZ3pJLk6d-CNMEnJtKz1Wu8N3aUeBXTxaYY',1,'2022-02-09 18:30:46'),(6,'gPo8E-sjNvyJbxEu8a-2CaLFpFwaLZU9XuB8BXVCoJk',4,'2022-02-09 18:32:18');
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_un` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'user1','password'),(2,'user2','password'),(3,'user3','password'),(4,'user4','password'),(5,'user5','password');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'my_first_full_stack'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-09 18:50:24
