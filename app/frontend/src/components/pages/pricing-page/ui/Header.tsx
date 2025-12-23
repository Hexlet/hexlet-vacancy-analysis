import { Group, Text, Anchor, ThemeIcon, Flex, rem, Box } from "@mantine/core";
import { ArrowTrendingUpIcon } from "@heroicons/react/16/solid";
import { HomeIcon } from "@heroicons/react/24/outline";

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
      <ArrowTrendingUpIcon color="#4ECDC4" />
     </ThemeIcon>
     <Text fw={700} size="md" lh={1}>
      Skill Pulse
     </Text>
    </Flex>
    <Flex align="center" gap="30px">
    <Anchor href="/" c="white">
       <Text fw={600} c="white">Для агенств</Text>
     </Anchor>
     <Anchor href="/" c="white">
      <Flex align="center" ta="center" gap={rem(4)}>
       <ThemeIcon color="#0A192F">
        <HomeIcon />
       </ThemeIcon>
       <Text fw={600}>На главную</Text>
      </Flex>
     </Anchor>
    </Flex>
   </Group>
  </Box>
 );
};

export default Header;

