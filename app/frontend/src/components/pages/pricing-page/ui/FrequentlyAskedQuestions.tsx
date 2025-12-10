import {
 Title,
 Text,
 Flex,
 ThemeIcon,
 Card,
 Container,
} from "@mantine/core";
import { QuestionMarkCircleIcon } from "@heroicons/react/24/outline";
import { faqData } from "../api/data";

interface FaqCardProps {
 question: string;
 answer: string;
}

export const FaqCard: React.FC<FaqCardProps> = ({ question, answer }) => {
 return (
  <Card
   shadow="sm"
   padding="lg"
   radius="md"
   withBorder
   style={{
    width: "450px",
    borderColor: "#e0e0e0",
    backgroundColor: "white",
   }}
  >
   <Flex gap="5px">
    <ThemeIcon color="#4ECDC4" variant="light" radius="xl" size="md">
     <QuestionMarkCircleIcon color="#4ECDC4" />
    </ThemeIcon>
    <Text fw="700" size="md" c="dark">
     {question}
    </Text>
   </Flex>
   <Text size="sm" c="dimmed" style={{ paddingLeft: "32px" }}>
    {answer}
   </Text>
  </Card>
 );
};



const FrequentlyAskedQuestions = () => {
 return (
  <Container size="md" py="xl">
   <Title order={2} ta="center" mb="xl" c="dark">
    Часто задаваемые вопросы
   </Title>
   
   <Flex gap="20px" wrap="wrap">
    {faqData.map((item) => (
     <FaqCard
      key={item.question}
      question={item.question}
      answer={item.answer}
     />
    ))}
   </Flex>
  </Container>
 );
};


export default FrequentlyAskedQuestions;
