import { Stack, Flex } from "@mantine/core";
import { Provider } from "react-redux";
import { store } from "../../../../store/store";

import PopularVacanciesCard from "./PopularVacanciesCards";
import LeftSideHeroSection from "./LeftSideHeroSection";

const HeroSection = () => {
 return (
  <Provider store={store}>
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
     <LeftSideHeroSection />
     <PopularVacanciesCard />
    </Flex>
   </Stack>
  </Provider>
 );
};

export default HeroSection;
