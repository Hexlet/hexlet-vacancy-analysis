import { Link } from '@inertiajs/react';
import { SocialIcon } from 'react-social-icons';
import { Send } from 'lucide-react';
import { useSubscriptionForm } from '../../../hooks/useSubscriptionForm';
import { TextInput, ActionIcon, Group, Text } from '@mantine/core';

const navSections = [
  {
    title: 'About',
    links: [
      { label: 'О нас', href: '/' },
      { label: 'Careers', href: '/careers' },
      { label: 'Partners', href: '/partners' },
    ],
  },
  {
    title: 'Support',
    links: [
      { label: 'FAQ', href: '/faq' },
      { label: 'Reviews', href: '/reviews' },
      { label: 'Contacts', href: '/contacts' },
    ],
  },
  {
    title: 'Legal',
    links: [
      { label: 'GDPR', href: '/gdpr' },
      { label: 'Privacy Policy', href: '/policy' },
    ],
  },
];

const NavColumn = ({ title, links }: { title: string; links: { label: string; href: string }[] }) => (
  <div className='text-left'>
    <h3 className="text-sm font-semibold text-gray-300 tracking-wider uppercase">
      {title}
    </h3>
    <ul className="mt-4 space-y-3">
      {links.map((link) => (
        <li key={link.label}>
          <Link href={link.href} className="text-gray-500 hover:text-white transition-colors duration-200">
            {link.label}
          </Link>
        </li>
      ))}
    </ul>
  </div>
);

const SubscriptionForm = () => {
  const { email, setEmail, status, message, handleSubmit } = useSubscriptionForm();

  return (
    <div className='text-left'>
      <Text size="sm" fw={700} className="text-gray-300 tracking-wider uppercase">
        Subscribe
      </Text>
      <form onSubmit={handleSubmit} className="mt-4">
        <Group gap="xs">
          <TextInput
            styles={{
              input: {
                backgroundColor: 'white',
                color: '#111827',
                borderColor: 'transparent',
              },
            }}
            placeholder="Ваш e-mail"
            required
            value={email}
            onChange={(event) => setEmail(event.currentTarget.value)}
            disabled={status === 'loading'}
            rightSection={
              <ActionIcon 
                type="submit" 
                size="lg" 
                color="blue" 
                variant="filled" 
                loading={status === 'loading'}
                aria-label="Subscribe"
              >
                <Send size={18} />
              </ActionIcon>
            }
          />
        </Group>
      </form>
      {message && (
        <Text
          size="sm"
          mt="xs"
          c={status === 'success' ? 'green' : 'red'}
        >
          {message}
        </Text>
      )}
      <div className="mt-6 flex space-x-3">
        <SocialIcon url="https://vk.com" target="_blank" rel="noopener noreferrer" style={{ height: 24, width: 24 }} bgColor="transparent" fgColor="#a0aec0" />
        <SocialIcon url="https://telegram.org" target="_blank" rel="noopener noreferrer" style={{ height: 24, width: 24 }} bgColor="transparent" fgColor="#a0aec0" />
      </div>
    </div>
  );
};


const Footer = () => {
  return (
    <footer className="bg-gray-950 text-gray-500">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {navSections.map((section) => (
            <NavColumn key={section.title} title={section.title} links={section.links} />
          ))}
          <SubscriptionForm />
        </div>

        <div className="mt-10 pt-8 border-t border-gray-800 flex flex-col sm:flex-row justify-between items-center text-sm">
          <p>© {new Date().getFullYear()} Your Company. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;