import { Title, Text, Stack, Flex, ThemeIcon, Card } from "@mantine/core";
import { featuresData, type FeatureCardData } from "../api/data";

interface FeatureCardProps {
 icon: FeatureCardData["icon"];
 title: FeatureCardData["title"];
 description: FeatureCardData["description"];
}

const FeatureCard: React.FC<FeatureCardProps> = (props) => {
 const Icon = props.icon;

 return (
  <Card
   padding="lg"
   radius="md"
   shadow="sm"
   bg="#0A192F"
   style={{
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    textAlign: "center",
    width: "300px",
    margin: "10px",
   }}
  >
   <ThemeIcon
    color="#1b5b6b"
    size="xl"
    radius="xl"
    mb="20px"
    style={{ width: "40px", height: "40px", padding: "5px" }}
   >
    <Icon color="#4ECDC4" />
   </ThemeIcon>
   <Text c="white" pb="10px" fz="xl">
    {props.title}
   </Text>
   <Text c="dimmed">{props.description}</Text>
  </Card>
 );
};

const WhatYouWillGet = () => {
 return (
  <Stack
   ml="auto"
   mr="auto"
   pt="25px"
   pb="40px"
   bg="#0A192F"
   style={{ maxWidth: "1120px", width: "100%", borderRadius: "8px" }}
  >
   <Title order={2} c="white" ta="center">
    {" "}
    Что вы получаете{" "}
   </Title>
   <Flex direction={{ base: "column", md: "row" }} align="center">
    {featuresData.map((feature) => (
     <FeatureCard
      key={feature.id}
      icon={feature.icon}
      title={feature.title}
      description={feature.description}
     />
    ))}
   </Flex>
  </Stack>
 );
};

export default WhatYouWillGet;
