import { ThemeIcon, Card, Title, Text, Flex, Stack } from "@mantine/core";
import { featuresData, hashmapForFeaturesIcons } from "../api/data";

export interface CardProps {
 title: string;
 text: string;
 iconEl: React.ElementType<React.SVGProps<SVGSVGElement>>;
}

const FeatureCard: React.FC<CardProps> = (props) => {
 const Icon = props.iconEl;

 return (
  <Card padding="lg" radius="md" shadow="sm" w="370px" h="205px">
   <ThemeIcon
    size="xl"
    variant="gradient"
    gradient={{ from: "#4ECDC4", to: "#00334d", deg: 90 }}
    mb="10px"
   >
    {Icon && <Icon color="white" width="30px" />}
   </ThemeIcon>

   <Title order={4} mb="10px">
    {props.title}
   </Title>
   <Text>{props.text}</Text>
  </Card>
 );
};

const featuresDataWithIcons = featuresData.features.map((feature) => {
 const feautureIcon = hashmapForFeaturesIcons[feature.icon];
 return { ...feature, iconEl: feautureIcon };
});

const FeaturesBlock = () => {
 return (
  <Stack
   align="center"
   mt="70px"
   mb="xl"
   px={{ base: "md", sm: "lg", md: "xl" }}
  >
   <Title
    order={2}
    c="#022545"
    ta="center"
    fz={{ base: "32px", xs: "38px", sm: "42px", md: "48px" }}
   >
    {featuresData.greeting}
   </Title>
   <Text c="grey" ta="center" mb="20px" maw="700px" fz="20px">
    {featuresData.description}
   </Text>
   <Flex
    wrap="wrap"
    gap="xl"
    justify="center"
    align="stretch"
    py="xl"
    w="100%"
    mih="400px"
   >
    {featuresDataWithIcons.map((feature) => (
     <FeatureCard key={feature.id} {...feature} />
    ))}
   </Flex>
  </Stack>
 );
};

export default FeaturesBlock;
