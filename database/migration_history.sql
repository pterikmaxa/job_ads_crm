/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.14-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: job_ads_crm
-- ------------------------------------------------------
-- Server version	10.11.14-MariaDB-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (1,'contenttypes','0001_initial','2026-06-11 07:55:46.105111'),
(2,'auth','0001_initial','2026-06-11 07:55:46.237487'),
(3,'admin','0001_initial','2026-06-11 07:55:46.268123'),
(4,'admin','0002_logentry_remove_auto_add','2026-06-11 07:55:46.291151'),
(5,'admin','0003_logentry_add_action_flag_choices','2026-06-11 07:55:46.296095'),
(6,'contenttypes','0002_remove_content_type_name','2026-06-11 07:55:46.322607'),
(7,'auth','0002_alter_permission_name_max_length','2026-06-11 07:55:46.336053'),
(8,'auth','0003_alter_user_email_max_length','2026-06-11 07:55:46.347591'),
(9,'auth','0004_alter_user_username_opts','2026-06-11 07:55:46.351841'),
(10,'auth','0005_alter_user_last_login_null','2026-06-11 07:55:46.368483'),
(11,'auth','0006_require_contenttypes_0002','2026-06-11 07:55:46.369562'),
(12,'auth','0007_alter_validators_add_error_messages','2026-06-11 07:55:46.373926'),
(13,'auth','0008_alter_user_username_max_length','2026-06-11 07:55:46.386194'),
(14,'auth','0009_alter_user_last_name_max_length','2026-06-11 07:55:46.396509'),
(15,'auth','0010_alter_group_name_max_length','2026-06-11 07:55:46.407293'),
(16,'auth','0011_update_proxy_permissions','2026-06-11 07:55:46.411623'),
(17,'auth','0012_alter_user_first_name_max_length','2026-06-11 07:55:46.423744'),
(18,'sources','0001_initial','2026-06-11 07:55:46.444741'),
(19,'sources','0002_country_alter_jobsite_country_and_more','2026-06-11 07:55:46.539901'),
(20,'cvs','0001_initial','2026-06-11 07:55:46.545614'),
(21,'cvs','0002_alter_cvprofile_country','2026-06-11 07:55:46.588389'),
(22,'sessions','0001_initial','2026-06-11 07:55:46.601471'),
(23,'sources','0003_seed_initial_countries','2026-06-11 07:55:46.613209'),
(24,'sources','0004_alter_jobsite_color_status','2026-06-11 07:55:46.616205'),
(25,'sources','0005_recalculate_jobsite_color_status','2026-06-11 07:55:46.625226'),
(26,'vacancies','0001_initial','2026-06-11 07:55:46.657296'),
(27,'vacancies','0002_alter_jobpost_country','2026-06-11 07:55:46.717624'),
(28,'vacancies','0003_jobpoststatus_alter_jobpost_options','2026-06-27 19:31:24.019374'),
(29,'sources','0006_searchtechnology_alter_country_options_and_more','2026-06-27 19:45:03.234845'),
(30,'vacancies','0004_company_lead_leadaction_leadresponse','2026-07-09 20:05:53.156325');
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-22 21:25:19
