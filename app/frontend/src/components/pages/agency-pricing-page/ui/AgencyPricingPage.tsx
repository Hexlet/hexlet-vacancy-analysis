import { Box, Flex, Stack } from "@mantine/core";
import "@mantine/core/styles.css";

import BusinessAdvantages from "./BusinessAdvantages";
import ContactForm from "./ContactForm";
import PricingSection from "./PricingSection";
import Header from "./Header";

const AgencyPricingPage = () => {
 return (
  <>
   <Header/>
   <Box
   style={{
    backgroundColor: "white",
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "flex-start",
    padding: "20px",
    boxSizing: "border-box",
   }}
  >
   <Stack style={{ maxWidth: "1140px", width: "100%" }}>
    <PricingSection />
    <Flex
     gap="xl"
     wrap="wrap"
     justify="center"
     align="flex-start"
     style={{
      backgroundColor: "#0A192F",
      padding: "calc(2rem)",
      borderRadius: "10px",
      width: "100%",
     }}
    >
     <Box style={{ flex: 1, minWidth: "350px" }}>
      <BusinessAdvantages />
     </Box>
     <Box style={{ flex: 1, minWidth: "350px" }}>
      <ContactForm />
     </Box>
    </Flex>
   </Stack>
  </Box>
  </>
 );
}

export default AgencyPricingPage;
