import { Flex, Text, Card } from "@mantine/core";
import { motion } from "motion/react";

import { type StaticticsCardProp, statictiscCardsData } from "../api/data";

const formatValue = (value: number, suffix: string): string => {
 if (value >= 1000) {
  const formattedValue = (value / 1000).toFixed(1);
  const finalValue = formattedValue.endsWith(".0")
   ? formattedValue.slice(0, -2)
   : formattedValue;
  return `${finalValue}К${suffix}`;
 } else {
  return `${value}${suffix}`;
 }
};

const StatictiscCard = (props: StaticticsCardProp) => {
 const topSideOfCard = formatValue(props.value, props.suffix);

 return (
  <Card bg="transparent" p="0" style={{ width: "150px" }}>
   <motion.div
    initial={{ opacity: 0, y: -20 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{
     once: false,
     amount: 0.5,
    }}
    transition={{ duration: 0.6, ease: "easeOut" }}
   >
    <Text fz="30px" fw="700" c="#4ECDC4">
     {topSideOfCard}
    </Text>
   </motion.div>
   <Text fz="14px" c="white">
    {props.label}
   </Text>
  </Card>
 );
};

const StatictiscBlock = () => {
 return (
  <Flex
   align="center"
   justify="center"
   gap={{ base: "lg", sm: "40px" }}
   pt="xl"
   maw={{ base: "100%", sm: "500px" }}
   mx={{ base: "auto", md: 0 }}
   bg="linear-gradient(120deg, #082c4c, #4ECDC4)"
  >
   {statictiscCardsData.map((statictic) => (
    <StatictiscCard key={statictic.id} {...statictic} />
   ))}
  </Flex>
 );
};

export default StatictiscBlock;
