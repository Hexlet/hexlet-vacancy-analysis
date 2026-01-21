import { Stack, Flex, Box, Title, Text, Button } from "@mantine/core";
import { RocketLaunchIcon, PlayIcon } from "@heroicons/react/24/outline";
import PopularVacanciesCard from "./PopularVacanciesCard";
import StatictiscBlock from "./StatisticsBlock";

const HeroSection = () => {
 return (
  <Stack
   c="white"
   style={{
    width: "100%",
    background: "linear-gradient(120deg, #082c4c, #4ECDC4)",
   }}
   py={{ base: "md", md: "xl" }}
  >
   <Flex
    direction={{ base: "column", md: "row" }}
    justify={{ base: "center", md: "space-between" }}
    align={{ base: "center", md: "flex-start" }}
    gap={{ base: "xl", md: "100px" }}
    style={{ maxWidth: "1300px", width: "100%", margin: "0 auto" }}
    px={{ base: "md", sm: "lg", md: "xl" }}
   >
    <Box w={{ base: "100%", md: "600px" }} ta={{ base: "center", md: "left" }}>
     <Title
      order={1}
      fz={{ base: "42px", sm: "48px", md: "54px" }}
      lh={{ base: 1.2, md: 1.1 }}
      c="transparent"
      style={{
       backgroundImage: "linear-gradient(white, white, #39c0c3, #86e1e2)",
       backgroundClip: "text",
      }}
      mb="md"
     >
      Skill Pulse &mdash;
      <br />
      твой билет на рынок труда
     </Title>
     <Text
      fz={{ base: "md", sm: "lg", md: "xl" }}
      mb="xl"
      maw={{ base: "100%", sm: "520px" }}
      mx={{ base: "auto", md: 0 }}
     >
      Отслеживайте вакансии, анализируйте зарплаты и планируйте карьеру с
      помощью современной аналитической платформы{" "}
     </Text>

     <Flex
      gap="lg"
      direction={{ base: "column", sm: "row" }}
      pb="xl"
      style={{
       borderBottom: "1px solid #ccc",
      }}
      maw={{ base: "100%", sm: "530px" }}
      mx={{ base: "auto", md: 0 }}
     >
      <Button
       leftSection={<RocketLaunchIcon width="20px" />}
       style={{
        backgroundColor: "#4ECDC4",
        transition: "background-color 0.3s",
       }}
       fullWidth
       aria-label="Попробовать бесплатно"
       onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#3BB2A0")}
       onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "#4ECDC4")}
       size="md"
      >
       Попробовать бесплатно
      </Button>
      <Button
       leftSection={<PlayIcon width="20px" />}
       style={{
        backgroundColor: "white",
        color: "black",
        transition: "background-color 0.3s",
       }}
       fullWidth
       aria-label="Смотреть демо"
       onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#F0F0F0")}
       onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "white")}
       size="md"
      >
       Смотреть демо
      </Button>
     </Flex>
     <StatictiscBlock />
    </Box>

    <PopularVacanciesCard />
   </Flex>
  </Stack>
 );
};

export default HeroSection;
