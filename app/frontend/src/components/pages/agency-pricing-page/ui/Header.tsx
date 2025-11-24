import { Group, Text, Anchor, ThemeIcon, Flex, rem, Box } from "@mantine/core";

import { IconHome, IconTrendingUp } from "@tabler/icons-react";

const Header = () => {
 return (
  <Box
   component="header"
   bg="#0A192F"
   style={{
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    color: "white",
    height: 60,
    width: "100%",
   }}
  >
   <Group
    justify="space-between"
    style={{ maxWidth: "1100px", width: "100%", padding: "0 1rem" }}
   >
    <Flex align="center" gap="10px">
     <ThemeIcon color="#0A192F">
      <IconTrendingUp color="#4ECDC4" />
     </ThemeIcon>
     <Text fw={700} size="md" lh={1}>
      Skill Pulse
     </Text>
    </Flex>
    <Anchor href="/" c="white" underline="never">
     <Flex align="center" ta="center" gap={rem(4)}>
      <ThemeIcon color="#0A192F">
       <IconHome />
      </ThemeIcon>
      <Text>На главную</Text>
     </Flex>
    </Anchor>
   </Group>
  </Box>
 );
};

export default Header;
